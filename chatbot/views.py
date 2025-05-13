from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
import re
from .models import ChatMessage, ChatbotResponse

# Create your views here.

@login_required
@csrf_exempt
def chatbot_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip().lower()
            
            # Save user message
            chat_message = ChatMessage(
                user=request.user,
                message=user_message
            )
            
            # Find matching response pattern
            response = None
            for pattern in ChatbotResponse.objects.all():
                if re.search(pattern.query_pattern.lower(), user_message):
                    response = pattern.response
                    break
            
            # Default response if no pattern matches
            if not response:
                response = "I'm sorry, I don't have information about that. You can ask me about Netflix shows, movies, account issues, or streaming quality."
            
            chat_message.response = response
            chat_message.save()
            
            return JsonResponse({
                'response': response
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def chat_history(request):
    messages = ChatMessage.objects.filter(user=request.user).order_by('-created_at')[:50]
    return JsonResponse({
        'messages': [
            {
                'message': msg.message,
                'response': msg.response,
                'timestamp': msg.created_at.isoformat()
            }
            for msg in messages
        ]
    })
