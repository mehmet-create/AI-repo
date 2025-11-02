# chat_app/urls.py
from django.urls import path
from .views import AgentWebhookView

urlpatterns = [
    # The full path will be: [Your Domain]/webhook/
    path('webhook/', AgentWebhookView.as_view(), name='agent_webhook'),
]