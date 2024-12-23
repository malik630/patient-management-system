from tokenize import TokenError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import LoginSerializer, LogoutSerializer, UserCreateSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class AuthenticationViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        method='post',
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Authentification réussie",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'user': openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'username': openapi.Schema(type=openapi.TYPE_STRING),
                                'email': openapi.Schema(type=openapi.TYPE_STRING),
                                'role': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        ),
                        'tokens': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                                'access': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        )
                    }  
                )
            ),
            401: 'Identifiants invalides',
            403: 'Compte désactivé'
        }
    )

    @action(detail=False, methods=['post'])
    def login_view(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
        
            user = authenticate(request, username=username, password=password)
        
            if user is not None:
                if not user.is_active:
                    return Response({
                        'error': 'User account is disabled'
                    }, status=status.HTTP_403_FORBIDDEN)
            
                # Génération du token JWT
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Authentification réussie',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'role': user.role,
                        'first_name': user.first_name,
                        'last_name': user.last_name
                    },
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Identifiants invalides'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['post'])
    def register_view(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                # Générer les tokens comme dans votre login_view
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Inscription réussie',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'role': user.role,
                        'first_name': user.first_name,
                        'last_name': user.last_name
                    },
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    }
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        method='post',
        request_body=LogoutSerializer,
        responses={
            200: 'Déconnexion réussie',
            400: 'Token invalide'
        }
    )

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout_view(self, request):
        """
        Cette méthode permet à l'utilisateur de se déconnecter en invalidant son refresh_token.
        """
        
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Déconnexion réussie"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Token invalide"}, status=status.HTTP_400_BAD_REQUEST)