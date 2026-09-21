# ai_agent/urls.py
from django.urls import path
from .views import agent_chat_view

app_name = 'ai_agent'

urlpatterns = [
    path('chat/', agent_chat_view, name='agent_chat'),
]