from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

from ..models import Conversation, ChatMessage
from ..serializers import ChatMessageSerializer
from ..services_new import chat_with_gemini


class ChatMessageAPIView(APIView):
    """
    API endpoint for chat messages.
    
    Supports creating new conversations and adding messages to existing ones.
    """

    def post(self, request):
        """
        Send a message to the AI and get a response.
        """
        try:
            data = JSONParser().parse(request)
        except Exception as e:
            return Response(
                {'error': f'Invalid JSON: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        conversation_id = data.get('conversationId')
        message = data.get('message')

        if not message:
            return Response(
                {'error': 'Message is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not isinstance(message, str) or not message.strip():
            return Response(
                {'error': 'Message must be a non-empty string'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Get or create conversation
            if conversation_id:
                try:
                    conversation = Conversation.objects.get(id=conversation_id)
                except Conversation.DoesNotExist:
                    return Response(
                        {'error': f'Conversation with id {conversation_id} not found'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                # Create new conversation with first message as title (truncated)
                title = message[:50] + "..." if len(message) > 50 else message
                conversation = Conversation.objects.create(title=title)

            # Get existing messages for context
            chat_messages = list(conversation.messages.all().order_by('created_at'))

            # Build messages list for AI
            messages = []
            for chat_message in chat_messages:
                messages.append({
                    'role': chat_message.role,
                    'content': chat_message.content
                })

            # Add the new user message
            messages.append({
                'role': 'user',
                'content': message
            })

            # Save the user message to the database
            ChatMessage.objects.create(
                conversation=conversation,
                role='user',
                content=message
            )

            # Get response from AI (synchronous call)
            response = chat_with_gemini(messages)

            # Save the AI response to the database
            ChatMessage.objects.create(
                conversation=conversation,
                role='model',
                content=response
            )

            return Response({
                'conversationId': conversation.id,
                'message': response
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response(
                {'error': f'Validation error: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Chat failed: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get(self, request):
        """
        Get all messages for a conversation.
        """
        conversation_id = request.query_params.get('conversationId')

        if not conversation_id:
            return Response(
                {'error': 'Conversation ID is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Get conversation
            try:
                conversation = Conversation.objects.get(id=conversation_id)
            except Conversation.DoesNotExist:
                return Response(
                    {'error': f'Conversation with id {conversation_id} not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # Get messages
            messages = list(conversation.messages.all().order_by('created_at'))

            # Serialize messages
            serializer = ChatMessageSerializer(messages, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve messages: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )