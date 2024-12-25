from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from authentification.models import User

# Serializer pour l'authentification
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        write_only=True,
        required=True,
        min_length=3,
        max_length=50
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8
    )

    def validate(self, attrs):
        if not attrs.get('username') or not attrs.get('password'):
            raise serializers.ValidationError(
                "Les champs username et password sont requis."
            )
        return attrs
    
# Serializer pour la création d'un utilisateur
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'password', 'role', 'first_name', 'last_name']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
# Serializer pour la déconnexion
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()