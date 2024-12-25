from rest_framework import serializers
from authentification.models import User
from .models import Medecin, Patient, DossierPatient
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = ['numero_securite_sociale', 'user', 'date_naissance', 'adresse', 'telephone', 'mutuelle', 'medecin_traitant', 'personne_contact_nom', 'personne_contact_telephone']

    def validate_numero_securite_sociale(self, value):
        # Vérification du format du NSS (15 chiffres)
        if not value.isdigit() or len(value) != 15:
            raise serializers.ValidationError(
                "Le numéro de sécurité sociale doit contenir exactement 15 chiffres."
            )
        # Vérification de l'unicité
        if Patient.objects.filter(numero_securite_sociale=value).exists():
            raise serializers.ValidationError(
                "Ce numéro de sécurité sociale existe déjà dans la base de données."
            )
        return value

    def validate_telephone(self, value):
        # Vérification du format du numéro de téléphone
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError(
                "Le numéro de téléphone doit contenir exactement 10 chiffres."
            )
        return value

    def create(self, validated_data):
        try:
            # Création du patient
            patient = Patient.objects.create(
                **validated_data
            )
            return patient
        except Exception as e:
            raise serializers.ValidationError(f"Erreur lors de la création du patient: {str(e)}")
    
class DossierPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierPatient
        fields = ['NSS', 'date_derniere_mise_a_jour']

    def validate_NSS(self, value):
        # Vérification que le NSS correspond à un patient existant
        if not Patient.objects.filter(numero_securite_sociale=value).exists():
            raise serializers.ValidationError(
                "Aucun patient trouvé avec ce numéro de sécurité sociale."
            )
        # Vérification qu'un dossier n'existe pas déjà pour ce NSS
        if DossierPatient.objects.filter(NSS=value).exists():
            raise serializers.ValidationError(
                "Un dossier existe déjà pour ce patient."
            )
        return value

    def create(self, validated_data):
        try:
            dossier = DossierPatient.objects.create(**validated_data)
            return dossier
        except Exception as e:
            raise serializers.ValidationError(f"Erreur lors de la création du dossier: {str(e)}")

