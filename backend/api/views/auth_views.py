import logging
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

logger = logging.getLogger(__name__)
User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login a user and return a token
    """
    logger.info(f"Login view called with method: {request.method}")
    logger.info(f"Request data keys: {list(request.data.keys()) if request.data else 'No data'}")

    username = request.data.get('username')
    password = request.data.get('password')

    logger.info(f"Username: {username}, Password present: {bool(password)}")
    
    if not username or not password:
        return Response({'error': 'Please provide both username and password'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if not user:
        return Response({'error': 'Invalid credentials'}, 
                        status=status.HTTP_401_UNAUTHORIZED)
    
    # Get or create token
    token, created = Token.objects.get_or_create(user=user)
    
    # Return user data and token
    return Response({
        'token': token.key,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': 'admin' if user.is_staff else 'user'
        }
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Register a new user and return a token
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not username or not email or not password:
        return Response({'error': 'Please provide username, email, and password'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    # Create user
    user = User.objects.create_user(username=username, email=email, password=password)
    
    # Get or create token
    token, created = Token.objects.get_or_create(user=user)
    
    # Return user data and token
    return Response({
        'token': token.key,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': 'user'
        }
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_token_view(request):
    """
    Verify that a token is valid
    """
    return Response({'valid': True})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_view(request):
    """
    Get the current user's data
    """
    user = request.user
    
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': 'admin' if user.is_staff else 'user'
    })