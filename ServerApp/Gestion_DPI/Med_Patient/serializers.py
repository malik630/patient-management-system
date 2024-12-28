from rest_framework import serializers
from authentification.models import User
from .models import Patient, DossierPatient, Consultation, Ordonnance, Medicament, MedicamentOrdonnance, Examen
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
        fields = ['NSS', 'date_derniere_mise_a_jour', 'antecedents']

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
        
class MedicamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicament
        fields = ['id', 'nom', 'description']        
        
class MedicamentOrdonnanceSerializer(serializers.ModelSerializer):
    medicament = MedicamentSerializer(read_only=True)
    
    class Meta:
        model = MedicamentOrdonnance
        fields = ['medicament', 'dose', 'frequence', 'duree']

class OrdonnanceSerializer(serializers.ModelSerializer):
    medicaments = MedicamentOrdonnanceSerializer(source='medicament_ordonnances', many=True)
    description = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = Ordonnance
        fields = ['date_ordonnance', 'description', 'medicaments']

class ExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examen
        fields = ['type_examen', 'date_examen', 'bilan']

class ConsultationSerializer(serializers.ModelSerializer):
    ordonnance = OrdonnanceSerializer(read_only=True)
    examens = ExamenSerializer(many=True, read_only=True)
    medecin_nom = serializers.CharField(source='medecin.user.get_full_name', read_only=True)

    class Meta:
        model = Consultation
        fields = ['date_consultation', 'diagnostic', 'resume', 'medecin_nom', 'ordonnance', 'examens']

class ConsultationDossierPatientSerializer(serializers.ModelSerializer):
    consultations = ConsultationSerializer(many=True, read_only=True)
    
    class Meta:
        model = DossierPatient
        fields = ['date_derniere_mise_a_jour', 'antecedents', 'consultations']

class PatientDossierSerializer(serializers.ModelSerializer):
    dossier = ConsultationDossierPatientSerializer(source='dossierpatient')
    nom = serializers.CharField(source='user.last_name')
    prenom = serializers.CharField(source='user.first_name')
    medecin_traitant_nom = serializers.SerializerMethodField()

    def get_medecin_traitant_nom(self, obj):
        if obj.medecin_traitant and obj.medecin_traitant.user:
            return obj.medecin_traitant.user.get_full_name()
        return None
    class Meta:
        model = Patient
        fields = [
            'numero_securite_sociale', 'nom', 'prenom', 'date_naissance', 
            'adresse', 'telephone', 'mutuelle', 'medecin_traitant_nom',
            'personne_contact_nom', 'personne_contact_telephone', 'dossier'
        ]        

class ConsultationCreateSerializer(serializers.ModelSerializer):
    medicaments = MedicamentOrdonnanceSerializer(many=True, required=False)
    examens = ExamenSerializer(many=True, required=False)
    resume_medecin = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Consultation
        fields = ['diagnostic', 'medicaments', 'examens', 'resume_medecin']

    def validate(self, data):
        if not data.get('diagnostic') and not data.get('examens'):
            raise serializers.ValidationError(
                "Il faut soit un diagnostic avec médicaments, soit des examens"
            )
        if data.get('diagnostic') and not data.get('medicaments'):
            raise serializers.ValidationError(
                "Un diagnostic nécessite une prescription de médicaments"
            )
        if data.get('diagnostic') and data.get('examens'):
            raise serializers.ValidationError(
                "Un diagnostic et un bilan d'examen ne peuvent pas se faire en même temps"
            )
        if data.get('medicaments') and data.get('examens'):
            raise serializers.ValidationError(
                "Vous ne pouvez pas prescrire des médicaments et proposer un bilan d'examen en même temps."
            )
        if not data.get('resume_medecin'):
            raise serializers.ValidationError(
                "Le résumé de la consultation est obligatoire"
            )
        return data
