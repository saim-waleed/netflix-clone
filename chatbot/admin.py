from django.contrib import admin
from .models import ChatMessage, ChatbotResponse

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'response', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'message', 'response')
    readonly_fields = ('created_at',)

@admin.register(ChatbotResponse)
class ChatbotResponseAdmin(admin.ModelAdmin):
    list_display = ('query_pattern', 'response', 'created_at', 'updated_at')
    search_fields = ('query_pattern', 'response')
    readonly_fields = ('created_at', 'updated_at')
