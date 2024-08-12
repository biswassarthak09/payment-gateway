from django.urls import path

from . import views

urlpatterns = [
    path("initiate_payment/", views.initiate_payment, name = "initiate_payment"),
    path("callback/", views.process_callback, name = "process_callback"),
    path("csrf_token/", views.csrf_token_view, name = "csrf_token"),  # Add this line to enable CSRF protection.
]