from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if User.objects.filter(username=username).exists():
        return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

    user = User(username=username)
    user.set_password(password)
    user.save()
    token = Token.objects.create(user=user)
    return Response({"token": token.key}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)
    return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "This is a protected view!"}, status=status.HTTP_200_OK)