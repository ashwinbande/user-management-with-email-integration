from django.urls import path
from .views import NylasWebhookView

urlpatterns = [
    path('', NylasWebhookView.as_view(), name='webhook'),
]