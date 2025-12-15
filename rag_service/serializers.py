from rest_framework import serializers
from .models import UserDocument, ChatHistory
import os


class UserDocumentSerializer(serializers.ModelSerializer):
    """Serializer for viewing user documents."""
    class Meta:
        model = UserDocument
        fields = ['id', 'title', 'file', 'uploaded_at', 'processed', 'chunk_count']
        read_only_fields = ['processed', 'chunk_count', 'uploaded_at']


class UserDocumentUploadSerializer(serializers.ModelSerializer):
    """Serializer for uploading documents."""
    class Meta:
        model = UserDocument
        fields = ['file']

    def create(self, validated_data):
        upload_file = validated_data.get('file')
        title = os.path.splitext(upload_file.name)[0]
        return UserDocument.objects.create(
            user=self.context['request'].user,
            title=title,
            file=upload_file
        )
    
    def validate_file(self, value):
        ext = os.path.splitext(value.name)[1].lower()
        allowed_extensions = ['.pdf', '.txt', '.docx']
        
        if ext not in allowed_extensions:
            raise serializers.ValidationError(
                f"Only {', '.join(allowed_extensions)} files are allowed"
            )
        
        max_size = 10 * 1024 * 1024  # 10MB
        if value.size > max_size:
            raise serializers.ValidationError("File size cannot exceed 10MB")
        
        return value


class ChatSerializer(serializers.Serializer):
    """Serializer for chat requests."""
    question = serializers.CharField(max_length=1000, help_text="The question to ask the chatbot")
    chat_history = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        default=list,
        help_text="Optional conversation history"
    )


class ChatHistorySerializer(serializers.ModelSerializer):
    """Serializer for chat history responses."""
    class Meta:
        model = ChatHistory
        fields = ['id', 'query', 'response', 'created_at']