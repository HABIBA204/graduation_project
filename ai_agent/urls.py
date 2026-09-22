# ai_agent/urls.py
from django.urls import path
from .views import agent_chat_view
from . import views

app_name = 'ai_agent'

urlpatterns = [
    path('chat/', agent_chat_view, name='agent_chat'),
    path('purchase-order/<int:order_id>/approve/',views.approve_purchase_order,name='approvr_purchase_order')
]