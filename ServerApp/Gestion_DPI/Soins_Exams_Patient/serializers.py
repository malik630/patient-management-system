from rest_framework import serializers
from Med_Patient.models import Ordonnance, MedicamentOrdonnance, Medicament

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