from django.urls import path
from . import views

urlpatterns = [
    path('message/', views.chatbot_message, name='chatbot_message'),
    path('history/', views.chat_history, name='chat_history'),
] 