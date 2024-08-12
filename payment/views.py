import hmac
import hashlib
import requests
import json

from django.middleware.csrf import get_token
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework import response, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from .serializers.initiate_request_serializers import PayloadSerializer, RequestSerializer
from .serializers.paytabs_serializers import PaymentInitatePayloadSerializer
from .serializers.callback_request_serializers import CallbackSerializer
from .dtos.payment_initiate_payload import PaymentInitatePayload, CustomerDetailsDTO
from .enums.transaction_enums import TransactionClass, TransactionType, TransactionStatus, PaymentMethod
from .models import Config, Request
from dataclasses import asdict
from .constants import status_mapping
from .kafka import kafka_producer

@api_view(['GET'])
def csrf_token_view(request):
   token = get_token(request)
   return JsonResponse({'csrfToken': token})

@api_view(['POST'])
def initiate_payment(request):
   payload = request.data

   # Serialize the data
   serializer = PayloadSerializer(data=payload)
   
   if serializer.is_valid():
      paytabs_payload = generate_initiate_payment_payload(serializer.data)

      # Convert the dataclass to a dictionary
      payload_dict = asdict(paytabs_payload)
      paytabs_serializer = PaymentInitatePayloadSerializer(data=payload_dict)

      if paytabs_serializer.is_valid():
         try:
            response_data = generate_payment_url(payload_dict)
            url_response = record_response(response_data)

            record_serializer = RequestSerializer(data=url_response)
            if record_serializer.is_valid():
               record_serializer.save()
               return response.Response(record_serializer.data, status=status.HTTP_200_OK)
            else:
               return response.Response(record_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
         except requests.exceptions.RequestException as e:
            return response.Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
         
@csrf_exempt
@api_view(['POST'])
def process_callback(request):
   validate_callback_response(request)
   payload = request.data

   try:
      serializer = CallbackSerializer(data=payload)
      
      if serializer.is_valid():
         process_payment(serializer.data)
      else:
         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      return JsonResponse({'status': 'success'}, status=status.HTTP_200_OK)
   except Exception as e:
      return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


         
def generate_initiate_payment_payload(data):
   customer_details = CustomerDetailsDTO(
      name = data['client_details']['name'],
      email = data['client_details']['email'],
      phone = data['client_details']['phone']
   )

   payment_config = Config.objects.first()

   payload = PaymentInitatePayload(
      profile_id = payment_config.profile_id,
      tran_type = TransactionType.get_value(payment_config.tran_type),
      tran_class = TransactionClass.get_value(payment_config.tran_class),
      cart_id = data['order_details']['cart_id'],
      cart_currency = payment_config.cart_currency,
      cart_amount = data['order_details']['amount'],
      cart_description = data['order_details']['description'],
      paypage_lang = payment_config.language,
      customer_details = customer_details,
      hide_shipping = payment_config.hide_shipping,
      callback = payment_config.callback_url,
      return_url = payment_config.return_url,
      tokenise = payment_config.tokenise,
      framed = payment_config.framed,
   )

   return payload


def generate_payment_url(payload):
   # Make a POST request to Paytabs
   url = settings.PAYTABS_PAYMENT_GATEWAY_BASE_URL + settings.PAYTABS_PAYMENT_GATEWAY_REQUEST_ENDPOINT

   headers = {
      'Content-Type': 'application/json',
      'authorization': settings.PAYTABS_API_KEY
   }

   response = requests.post(url, json=payload, headers=headers)
   response.raise_for_status()

   response_data = response.json()

   return response_data


def record_response(response_data):
   # Save the response data to the database
   return {
        'transaction_id': response_data.get('tran_ref'),
        'transaction_status': TransactionStatus.PENDING.value,
        'transaction_amount': response_data.get('cart_amount'),
        'transaction_currency': response_data.get('cart_currency'),
        'payment_method': PaymentMethod.CARD.value,
        'identifier': response_data.get('cart_id'),
        'profile_id': response_data.get('profileId'),
        'payment_url': response_data.get('redirect_url'),
   }


def validate_callback_response(request):
   secret = settings.PAYTABS_API_KEY
   signature = request.headers.get('signature')
   client_key = request.headers.get('client_key')

   # Validate the client key
   if client_key != settings.PAYTABS_CLIENT_KEY:
      raise ValidationError("Invalid client key")
   
   payload_dict = json.loads(request.body)
   payload_json = json.dumps(payload_dict, separators=(',', ':'))
   
   # Validate the signature
   expected_signature = hmac.new(
      secret.encode(),
      payload_json.encode(),
      hashlib.sha256
   ).hexdigest()

   if not hmac.compare_digest(signature, expected_signature):
      raise ValidationError("Invalid signature")
   

def process_payment(data):
   request = Request.objects.get(transaction_id=data['tran_ref'])

   # Update the transaction status
   request.transaction_status = status_mapping.get(data['payment_result']['response_status'], TransactionStatus.FAILED.value)

   record_serializer = RequestSerializer(request, data=request.__dict__, partial=True)

   if record_serializer.is_valid():
      record_serializer.save()

   # Prepare the Kafka message
   message = record_serializer.data

   # Send the payment status to Kafka
   kafka_producer.send_message('payment_status', message)

   
