import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import UserDocument, ChatHistory
from .serializers import (
    UserDocumentUploadSerializer,
    UserDocumentSerializer,
    ChatSerializer,
    ChatHistorySerializer,
)
from .personal_service import PersonalRAGService

logger = logging.getLogger(__name__)


class DocumentUploadView(APIView):
    """Upload documents for RAG processing."""
    
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        summary="Upload document",
        description="Upload a document (PDF, DOCX, TXT) for RAG processing.",
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'file': {
                        'type': 'string',
                        'format': 'binary',
                        'description': 'Document file (PDF, DOCX, TXT)'
                    }
                },
                'required': ['file']
            }
        },
        responses={201: UserDocumentSerializer}
    )
    def post(self, request):
        """Upload and process document."""
        serializer = UserDocumentUploadSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        document = serializer.save()
        
        try:
            service = PersonalRAGService(request.user.id)
            chunk_count = service.process_document(document.file.path, document.id)
            
            if chunk_count > 0:
                document.processed = True
                document.chunk_count = chunk_count
                document.save()
            
            return Response(UserDocumentSerializer(document).data, status=201)
        except Exception as e:
            document.delete()
            logger.error(f"Document processing failed: {e}")
            return Response({'error': 'Processing failed'}, status=500)


class ChatView(APIView):
    """Chat with the RAG-powered chatbot."""
    
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Send message to chatbot",
        description="Send a question and receive an AI-generated response based on your documents.",
        request=ChatSerializer,
        responses={200: OpenApiTypes.OBJECT}
    )
    def post(self, request):
        """Process user query and return AI response."""
        serializer = ChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        question = serializer.validated_data['question']
        chat_history = serializer.validated_data.get('chat_history', [])
        
        try:
            service = PersonalRAGService(request.user.id)
            result = service.query(question, chat_history)
            
            # Save to chat history
            ChatHistory.objects.create(
                user=request.user,
                query=question,
                response=result['answer']
            )
            
            return Response({
                'question': question,
                'answer': result['answer'],
                'sources': result.get('sources', [])
            })
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return Response({'error': str(e)}, status=500)


class ChatHistoryView(APIView):
    """Retrieve user's chat history."""
    
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get chat history",
        description="Retrieve the logged-in user's chat history.",
        responses={200: ChatHistorySerializer(many=True)}
    )
    def get(self, request):
        """Get user's chat history."""
        history = ChatHistory.objects.filter(user=request.user)[:50]
        serializer = ChatHistorySerializer(history, many=True)
        return Response(serializer.data)

