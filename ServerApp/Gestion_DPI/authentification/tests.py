import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User  # Ajustez le chemin d'import selon votre structure

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user():
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpassword123',
        first_name='Test',
        last_name='User',
        role='LR',
        is_active=True
    )

@pytest.mark.django_db
def test_login_success(api_client, test_user):
    """
    Test d'une authentification réussie avec le modèle User personnalisé
    """
    url = 'http://127.0.0.1:8000/api/auth/login_view/'
    
    data = {
        'username': 'testuser',
        'password': 'testpassword123'
    }
    
    response = api_client.post(url, data, format='json')
    
    assert response.status_code == status.HTTP_200_OK
    assert 'message' in response.data
    assert response.data['message'] == 'Authentification réussie'
    
    # Vérification des données utilisateur
    user_data = response.data['user']
    assert user_data['id'] == test_user.id
    assert user_data['username'] == test_user.username
    assert user_data['email'] == test_user.email
    assert user_data['role'] == test_user.role
    assert user_data['first_name'] == test_user.first_name
    assert user_data['last_name'] == test_user.last_name
    
    # Vérification des tokens
    assert 'tokens' in response.data
    assert 'access' in response.data['tokens']
    assert 'refresh' in response.data['tokens']

@pytest.mark.django_db
def test_login_invalid_credentials(api_client, test_user):
    """
    Test d'une authentification avec des identifiants invalides
    """
    url = 'http://127.0.0.1:8000/api/auth/login_view/'
    
    data = {
        'username': 'testuser',
        'password': 'wrongpassword'
    }
    
    response = api_client.post(url, data, format='json')
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'error' in response.data