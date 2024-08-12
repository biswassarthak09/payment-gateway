from rest_framework import serializers

class CustomerDetailsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=15)
    street1 = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=2)
    zip = serializers.CharField(max_length=10)
    ip = serializers.CharField(max_length=50)

class PaymentResultSerializer(serializers.Serializer):
    response_status = serializers.CharField(max_length=1)
    response_code = serializers.CharField(max_length=10)
    response_message = serializers.CharField(max_length=255)
    acquirer_ref = serializers.CharField(max_length=50)
    cvv_result = serializers.CharField(max_length=5, allow_blank=True)
    avs_result = serializers.CharField(max_length=5, allow_blank=True)
    transaction_time = serializers.CharField(max_length=50)

class PaymentInfoSerializer(serializers.Serializer):
    payment_method = serializers.CharField(max_length=50)
    card_type = serializers.CharField(max_length=10)
    card_scheme = serializers.CharField(max_length=20)
    payment_description = serializers.CharField(max_length=50)
    expiryMonth = serializers.IntegerField()
    expiryYear = serializers.IntegerField()

class CallbackSerializer(serializers.Serializer):
    tran_ref = serializers.CharField(max_length=20)
    merchant_id = serializers.IntegerField()
    profile_id = serializers.IntegerField()
    cart_id = serializers.CharField(max_length=20)
    cart_description = serializers.CharField(max_length=255)
    cart_currency = serializers.CharField(max_length=3)
    cart_amount = serializers.CharField(max_length=10)
    tran_currency = serializers.CharField(max_length=3)
    tran_total = serializers.CharField(max_length=10)
    tran_type = serializers.CharField(max_length=20)
    tran_class = serializers.CharField(max_length=20)
    customer_details = CustomerDetailsSerializer()
    payment_result = PaymentResultSerializer()
    payment_info = PaymentInfoSerializer()
    token = serializers.CharField(max_length=50)
    ipn_trace = serializers.CharField(max_length=50)
