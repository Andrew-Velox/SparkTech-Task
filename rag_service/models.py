from django.db import models
from django.conf import settings
import os

User = settings.AUTH_USER_MODEL


class UserDocument(models.Model):
    # Documents uploaded by users for RAG processing
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='user_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    chunk_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    def delete(self, *args, **kwargs):
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['-uploaded_at']


class ChatHistory(models.Model):
    # Stores messages 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_history')
    query = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.query[:50]}..."

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Chat Histories"