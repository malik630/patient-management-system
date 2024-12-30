from rest_framework import serializers
from Med_Patient.models import DossierPatient, Examen, Ordonnance, MedicamentOrdonnance, Medicament, Patient
from Soins_Exams_Patient.models import ResultatExamen

class MedicamentTraceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medicament
        fields = ['id', 'nom', 'description']  


class MedicamentOrdonnanceTraceSerializer(serializers.ModelSerializer):
    medicament = MedicamentTraceSerializer()
    
    class Meta:
        model = MedicamentOrdonnance
        fields = ['medicament', 'dose', 'frequence', 'duree']


class OrdonnancePharmacienSerializer(serializers.ModelSerializer):
    medicaments = MedicamentOrdonnanceTraceSerializer(
        source='medicament_ordonnances',
        many=True,
        read_only=True
    )
    patient_nss = serializers.CharField(source="consultation.dossier_patient.NSS.numero_securite_sociale", read_only=True)
    
    class Meta:
        model = Ordonnance
        fields = [
            'id',
            'date_ordonnance',
            'est_validee',
            'description',
            'patient_nss',
            'medicaments'
        ]

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['numero_securite_sociale', 'user', 'date_naissance', 'adresse', 
                 'telephone', 'mutuelle', 'medecin_traitant', 'personne_contact_nom', 
                 'personne_contact_telephone']

class DossierPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierPatient
        fields = '__all__'

class ExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examen
        fields = '__all__'

class ResultatExamenSerializer(serializers.ModelSerializer):
    date_examen = serializers.DateField(source='examen.date_examen', read_only=True)
    type_examen = serializers.CharField(source='examen.type_examen', read_only=True)
    laborantin_radiologue = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = ResultatExamen
        fields = [
            'id', 'examen', 'laborantin_radiologue', 'date_examen', 'type_examen',
            'glycemie', 'hypertension', 'fer', 'TSH', 'cholesterol',
            'compte_rendu', 'image_medicale'
        ]

    def validate_examen(self, value):
        """
        Vérifie que l'examen n'a pas déjà un résultat et correspond au type d'utilisateur
        """
        request = self.context.get('request')
        if not request or not request.user:
            raise serializers.ValidationError("Utilisateur non authentifié")

        try:
            laborantin_radiologue = request.user.laborantin_radiologue
        except:
            raise serializers.ValidationError("Utilisateur non autorisé")

        # Vérifier si l'examen a déjà un résultat
        if hasattr(value, 'resultat'):
            raise serializers.ValidationError("Cet examen a déjà un résultat")

        # Vérifier que le type d'examen correspond au rôle de l'utilisateur
        if laborantin_radiologue.role == 'Laborantain' and value.type_examen != 'biologique':
            raise serializers.ValidationError("Un laborantin ne peut traiter que des examens biologiques")
        elif laborantin_radiologue.role == 'Radiologue' and value.type_examen != 'radiologique':
            raise serializers.ValidationError("Un radiologue ne peut traiter que des examens radiologiques")

        return value        