from rest_framework import serializers
from payment.models import Request

class ClientDetailsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    phone = serializers.CharField(max_length=15)
    email = serializers.EmailField()

class OrderDetailsSerializer(serializers.Serializer):
    cart_id = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3)
    description = serializers.CharField(max_length=255)
    transaction_type = serializers.CharField(max_length=10)
    transaction_class = serializers.CharField(max_length=10)

class PayloadSerializer(serializers.Serializer):
    client_details = ClientDetailsSerializer()
    order_details = OrderDetailsSerializer()

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'
