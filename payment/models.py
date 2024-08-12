from django.db import models
from django.utils import timezone

class Config(models.Model):
    profile_id = models.IntegerField()
    tran_type = models.IntegerField(default=1)
    tran_class = models.IntegerField(default=1)
    cart_currency = models.CharField(max_length=3)
    language = models.CharField(max_length=3)
    hide_shipping = models.BooleanField(default=True)
    callback_url = models.URLField(blank=True)
    return_url = models.URLField(blank=True)
    tokenise = models.IntegerField(default=2)
    framed = models.BooleanField(default=True)

class Request(models.Model):
    transaction_id = models.CharField(max_length=20)
    transaction_status = models.CharField(max_length=10)
    transaction_amount = models.FloatField()
    transaction_currency = models.CharField(max_length=3)
    transaction_date = models.DateTimeField(default=timezone.now)
    payment_method = models.CharField(max_length=10)
    identifier = models.CharField(max_length=20)
    profile_id = models.IntegerField()
    payment_url = models.URLField(blank=True)
