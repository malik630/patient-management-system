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
from rest_framework.views import APIView
from Med_Patient.models import PersonnelAdministratif, Patient, Medecin
from Soins_Exams_Patient.models import Infirmier, Pharmacien, LaborantinRadiologue
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
    
    @swagger_auto_schema(
        method='post',
        request_body=LogoutSerializer,
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Ajouter le token d'accès dans ce format : Bearer <access_token>",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
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
        
class RegisterView(APIView):

    def create_user(self, data, role_model, **extra_fields):
        """
        Helper function to create a user and associate it with a specific role.
        """
        user_serializer = UserCreateSerializer(data=data)

        if user_serializer.is_valid():
            try:
                user = user_serializer.save()
                role_instance = role_model.objects.create(user=user, **extra_fields)
                refresh = RefreshToken.for_user(user)

                return Response({
                    'message': f'{role_model.__name__} crée avec succés.',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'role': user.role,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                    },
                    'tokens': {
                         'refresh': str(refresh),
                         'access': str(refresh.access_token)
                    },
                    'role_data': {
                        'id': role_instance.id,
                        **extra_fields
                    }
                }, status=status.HTTP_201_CREATED)
        
            except Exception as e:
                return Response({
                    'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        role = request.data.get('role')
        extra_fields = {}
        
        if role == 'PA': 
            extra_fields['telephone'] = request.data.get('telephone')
            extra_fields['poste'] = request.data.get('poste')
            return self.create_user(request.data, PersonnelAdministratif, **extra_fields)

        if role == 'P':
            extra_fields['numero_securite_sociale'] = request.data.get('numero_securite_sociale')
            extra_fields['date_naissance'] = request.data.get('date_naissance')
            extra_fields['adresse'] = request.data.get('adresse')
            extra_fields['telephone'] = request.data.get('telephone')
            extra_fields['mutuelle'] = request.data.get('mutuelle')
            return self.create_user(request.data, Patient, **extra_fields)

        if role == 'M':
            extra_fields['specialite'] = request.data.get('specialite')
            extra_fields['numero_telephone'] = request.data.get('numero_telephone')
            return self.create_user(request.data, Medecin, **extra_fields)

        elif role == 'I':
            extra_fields['telephone'] = request.data.get('telephone')
            return self.create_user(request.data, Infirmier, **extra_fields)

        elif role == 'PH':
            extra_fields['telephone'] = request.data.get('telephone')
            return self.create_user(request.data, Pharmacien, **extra_fields)

        elif role == 'LR':
            extra_fields['telephone'] = request.data.get('telephone')
            extra_fields['role'] = request.data.get('role_type')  # Laborantain ou Radiologue
            return self.create_user(request.data, LaborantinRadiologue, **extra_fields)

        return Response({'error': 'Invalid role specified'}, status=status.HTTP_400_BAD_REQUEST)        