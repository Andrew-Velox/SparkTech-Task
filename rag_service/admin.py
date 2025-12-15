from django.contrib import admin
from .models import UserDocument, ChatHistory


@admin.register(UserDocument)
class UserDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'uploaded_at', 'processed', 'chunk_count']
    list_filter = ['processed', 'uploaded_at']
    search_fields = ['title', 'user__username']


@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'query_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'query', 'response']
    
    def query_preview(self, obj):
        return obj.query[:50] + '...' if len(obj.query) > 50 else obj.query
    query_preview.short_description = 'Query'