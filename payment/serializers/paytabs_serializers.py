from rest_framework import serializers
from .initiate_request_serializers import ClientDetailsSerializer

class PaymentInitatePayloadSerializer(serializers.Serializer):
    profile_id = serializers.IntegerField()
    tran_type = serializers.CharField(max_length=8)
    tran_class = serializers.CharField(max_length=8)
    cart_id = serializers.CharField(max_length=10)
    cart_currency = serializers.CharField(max_length=3)
    cart_amount = serializers.FloatField()
    cart_description = serializers.CharField(max_length=255)
    paypage_lang = serializers.CharField(max_length=3)
    customer_details = ClientDetailsSerializer()
    hide_shipping = serializers.BooleanField()
    callback = serializers.URLField()
    return_url = serializers.URLField()
    tokenise = serializers.IntegerField()
    framed = serializers.BooleanField()
