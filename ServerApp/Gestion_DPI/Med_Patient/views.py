from django.forms import ValidationError
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .serializers import ConsultationCreateSerializer, PatientDossierSerializer, UserSerializer, PatientSerializer, DossierPatientSerializer
from .permissions import IsPersonnelAdministratif
from django.db import transaction
from datetime import date
from rest_framework.permissions import IsAuthenticated
from .models import Consultation, DossierPatient, Patient
from django.shortcuts import get_object_or_404
from .permissions import IsPatientUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class PersonnelAdministratifViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsPersonnelAdministratif]

     # Documentation Swagger
    @swagger_auto_schema(
        method='post',
        operation_summary="Créer un dossier patient informatisé (DPI)",
        operation_description=(
            "Cette fonction permet au personnel administratif de créer un dossier patient informatisé (DPI). "
            "Elle inclut la création d'un utilisateur, d'un patient et du dossier patient associé."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "user": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Données de l'utilisateur à créer",
                    properties={
                        "username": openapi.Schema(type=openapi.TYPE_STRING, description="Nom d'utilisateur"),
                        "email": openapi.Schema(type=openapi.TYPE_STRING, description="Email"),
                        "password": openapi.Schema(type=openapi.TYPE_STRING, description="Mot de passe"),
                        "first_name": openapi.Schema(type=openapi.TYPE_STRING, description="Prénom"),
                        "last_name": openapi.Schema(type=openapi.TYPE_STRING, description="Nom"),
                    },
                    required=["username", "email", "password", "first_name", "last_name"],
                ),
                "patient": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Données du patient à créer",
                    properties={
                        "numero_securite_sociale": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Numéro de sécurité sociale"
                        ),
                        "date_naissance": openapi.Schema(
                            type=openapi.TYPE_STRING, format="date", description="Date de naissance (YYYY-MM-DD)"
                        ),
                        "adresse": openapi.Schema(type=openapi.TYPE_STRING, description="Adresse"),
                        "telephone": openapi.Schema(type=openapi.TYPE_STRING, description="Numéro de téléphone"),
                        "mutuelle": openapi.Schema(type=openapi.TYPE_STRING, description="Nom de la mutuelle"),
                        "personne_contact_nom": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Nom de la personne de contact"
                        ),
                        "personne_contact_telephone": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Téléphone de la personne de contact"
                        ),
                    },
                    required=[
                        "numero_securite_sociale",
                        "date_naissance",
                        "adresse",
                        "telephone",
                        "mutuelle",
                        "personne_contact_nom",
                        "personne_contact_telephone",
                    ],
                ),
            },
            required=["user", "patient"],
        ),
        responses={
            201: openapi.Response(
                description="Création réussie",
                examples={
                    "application/json": {
                        "message": "Patient et dossier créés avec succès",
                        "user": {
                            "username": "test_patient",
                            "email": "test_patient@example.com",
                            "first_name": "test",
                            "last_name": "patient",
                        },
                        "patient": {
                            "numero_securite_sociale": "123456789000000",
                            "date_naissance": "1982-10-12",
                            "adresse": "123 Avenue des Champs",
                            "telephone": "0601020304",
                            "mutuelle": "Mutuelle B",
                            "personne_contact_nom": "Jane Doe",
                            "personne_contact_telephone": "0987654321",
                        },
                        "dossier": {
                            "NSS": "123456789000000",
                            "date_derniere_mise_a_jour": "2024-12-25",
                        },
                    }
                },
            ),
            400: openapi.Response(
                description="Erreur de validation",
                examples={
                    "application/json": {"error": "Les données utilisateur sont requises"}
                },
            ),
            403: openapi.Response(
                description="Accès refusé",
                examples={
                    "application/json": {
                        "error": "Accès non autorisé. Seul le personnel administratif peut créer des patients."
                    }
                },
            ),
            500: openapi.Response(
                description="Erreur interne",
                examples={"application/json": {"error": "Une erreur est survenue: <message_erreur>"}},
            ),
        },
    )
    
    @action(detail=False, methods=['post'])
    @transaction.atomic  # Assure que toutes les créations se font ou aucune
    def creer_DPI(self, request):
        try:
            # Vérification du rôle
            if not request.user.role == 'PA':
                return Response(
                    {'error': 'Accès non autorisé. Seul le personnel administratif peut créer des patients.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            # 1. Création de l'utilisateur
            user_data = request.data.get('user')
            if not user_data:
                return Response(
                    {'error': 'Les données utilisateur sont requises'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            user_serializer = UserSerializer(data=user_data)
            if not user_serializer.is_valid():
                return Response(
                    user_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            user = user_serializer.save()

            # 2. Création du patient
            patient_data = request.data.get('patient')
            if not patient_data:
                return Response(
                    {'error': 'Les données patient sont requises'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Ajout de l'ID utilisateur aux données patient
            patient_data['user'] = user.id
            patient_serializer = PatientSerializer(data=patient_data)
            if not patient_serializer.is_valid():
                # En cas d'erreur, on annule la création de l'utilisateur
                user.delete()
                return Response(
                    patient_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            patient = patient_serializer.save()

            # 3. Création du dossier patient
            dossier_data = {
                'NSS': patient.numero_securite_sociale,
                'date_derniere_mise_a_jour': date.today()
            }
            dossier_data = request.data.get('antecedants')
            dossier_serializer = DossierPatientSerializer(data=dossier_data)
            if not dossier_serializer.is_valid():
                return Response(
                    dossier_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            dossier = dossier_serializer.save()

            # Réponse avec toutes les données créées
            return Response({
                'message': 'Patient et dossier créés avec succès',
                'user': user_serializer.data,
                'patient': patient_serializer.data,
                'dossier': dossier_serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            # En cas d'erreur, la transaction est automatiquement annulée
            return Response(
                {'error': f'Une erreur est survenue: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class PatientDossierViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PatientDossierSerializer
    permission_classes = [IsAuthenticated, IsPatientUser]

    
    @swagger_auto_schema(
        operation_summary="Liste le dossier du patient connecté",
        operation_description="""Retourne le dossier médical complet du patient connecté.
        Nécessite une authentification et que l'utilisateur ait le rôle patient.""",
        responses={
            200: openapi.Response(
                description="Dossier patient récupéré avec succès",
                schema=PatientDossierSerializer
            ),
            401: "Non authentifié",
            403: "Pas les permissions requises (rôle patient requis)",
            404: "Patient non trouvé"
        },
        tags=['Dossier Patient'],
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Token JWT Bearer. Ex: Bearer {token}",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Récupère le dossier détaillé du patient",
        operation_description="""Retourne le dossier médical détaillé du patient connecté incluant :
        - Informations personnelles
        - Médecin traitant
        - Antécédents médicaux
        - Historique des consultations
        - Ordonnances et médicaments
        - Examens médicaux
        """,
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Token JWT Bearer. Ex: Bearer {token}",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Dossier détaillé récupéré avec succès",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'numero_securite_sociale': openapi.Schema(type=openapi.TYPE_STRING),
                        'nom': openapi.Schema(type=openapi.TYPE_STRING),
                        'prenom': openapi.Schema(type=openapi.TYPE_STRING),
                        'date_naissance': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                        'adresse': openapi.Schema(type=openapi.TYPE_STRING),
                        'telephone': openapi.Schema(type=openapi.TYPE_STRING),
                        'mutuelle': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                        'medecin_traitant_nom': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                        'personne_contact_nom': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                        'personne_contact_telephone': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                        'dossier': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'date_derniere_mise_a_jour': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                                'antecedents': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                'consultations': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'date_consultation': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                                            'diagnostic': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                            'resume': openapi.Schema(type=openapi.TYPE_STRING),
                                            'medecin_nom': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                            'ordonnance': openapi.Schema(
                                                type=openapi.TYPE_OBJECT,
                                                properties={
                                                    'date_ordonnance': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                                                    'medicaments': openapi.Schema(
                                                        type=openapi.TYPE_ARRAY,
                                                        items=openapi.Schema(
                                                            type=openapi.TYPE_OBJECT,
                                                            properties={
                                                                'medicament': openapi.Schema(
                                                                    type=openapi.TYPE_OBJECT,
                                                                    properties={
                                                                        'nom': openapi.Schema(type=openapi.TYPE_STRING),
                                                                        'description': openapi.Schema(type=openapi.TYPE_STRING, nullable=True)
                                                                    }
                                                                ),
                                                                'dose': openapi.Schema(type=openapi.TYPE_STRING),
                                                                'frequence': openapi.Schema(type=openapi.TYPE_STRING),
                                                                'duree': openapi.Schema(type=openapi.TYPE_STRING)
                                                            }
                                                        )
                                                    )
                                                }
                                            ),
                                            'examens': openapi.Schema(
                                                type=openapi.TYPE_ARRAY,
                                                items=openapi.Schema(
                                                    type=openapi.TYPE_OBJECT,
                                                    properties={
                                                        'type_examen': openapi.Schema(type=openapi.TYPE_STRING),
                                                        'date_examen': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                                                        'bilan': openapi.Schema(type=openapi.TYPE_STRING, nullable=True)
                                                    }
                                                )
                                            )
                                        }
                                    )
                                )
                            }
                        )
                    }
                )
            ),
            401: "Non authentifié",
            403: "Pas les permissions requises (rôle patient requis)",
            404: "Patient non trouvé"
        },
        tags=['Dossier Patient']
    )

    
    def get_queryset(self):
        # Retourne uniquement le patient correspondant à l'utilisateur connecté
        return Patient.objects.filter(user=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        # Récupère le patient de l'utilisateur connecté
        patient = get_object_or_404(Patient, user=request.user)
        serializer = self.get_serializer(patient)
        return Response(serializer.data) 

class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationCreateSerializer

    @action(detail=False, methods=['post'])
    def creer_consultation(self, request):
        """
        Endpoint pour créer une nouvelle consultation
        
        POST /api/consultations/creer_consultation/
        {
            "nss": "123456789",
            "diagnostic": "Rhinopharyngite",
            "description_ordonnance": "À prendre pendant les repas. Éviter l'alcool.",
            "resume_medecin": "Patient présentant une forte fièvre...",
            "medicaments": [
                {
                    "nom_medicament": "Doliprane",
                    "dose": "1000mg",
                    "frequence": "3 fois par jour",
                    "duree": "5 jours"
                }
            ]
        }
        """
        # Récupérer le patient et vérifier le médecin traitant
        nss = request.data.get('nss')
        patient = get_object_or_404(Patient, numero_securite_sociale=nss)
        
        if patient.medecin_traitant_id != request.user.medecin.id:
            raise ValidationError("Vous devez être le médecin traitant du patient")

        # Récupérer le dossier patient
        dossier = get_object_or_404(DossierPatient, NSS=patient)

        # Construire le résumé complet avec les antécédents obligatoires
        resume_complet = self._construire_resume_complet(
            dossier.antecedents,
            request.data.get('resume_medecin'),
            request.data.get('diagnostic'),
            request.data.get('medicaments', []),
            request.data.get('examens', [])
        )

        # Préparer les données de la consultation
        consultation_data = {
            'dossier_patient': dossier,
            'medecin': request.user.medecin,
            'date_consultation': date.today(),
            'diagnostic': request.data.get('diagnostic'),
            'resume': resume_complet
        }

        # Créer la consultation
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        consultation = Consultation.objects.create(**consultation_data)

        # Gérer l'ordonnance si diagnostic présent
        if consultation.diagnostic:
            ordonnance = Ordonnance.objects.create(
                consultation=consultation,
                date_ordonnance=date.today(),
                description=request.data.get('description_ordonnance')
            )
            
            for med_data in request.data.get('medicaments', []):
                medicament = get_object_or_404(Medicament, nom=med_data['nom_medicament'])
                MedicamentOrdonnance.objects.create(
                    medicament=medicament,
                    ordonnance=ordonnance,
                    dose=med_data['dose'],
                    frequence=med_data['frequence'],
                    duree=med_data['duree']
                )

        # Gérer les examens si présents
        for exam_data in request.data.get('examens', []):
            Examen.objects.create(
                consultation=consultation,
                **exam_data
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _construire_resume_complet(self, antecedents, resume_medecin, diagnostic, medicaments, examens):
        """Construit le résumé complet en incluant obligatoirement les antécédents"""
        resume_sections = [
            "=== ANTÉCÉDENTS DU PATIENT ===",
            antecedents,
            "\n=== RÉSUMÉ DE LA CONSULTATION ===",
            resume_medecin
        ]

        if diagnostic:
            resume_sections.extend([
                "\n=== DIAGNOSTIC ===",
                diagnostic
            ])

        if medicaments:
            for med in medicaments:
                resume_sections.append(
                    f"- {med['nom_medicament']}: {med['dose']}, "
                    f"{med['frequence']} pendant {med['duree']}"
                )

        if examens:
            resume_sections.extend([
                "\n=== EXAMENS PRESCRITS ==="
            ])
            for exam in examens:
                resume_sections.extend([
                    f"- Examen {exam['type_examen']} prévu le {exam['date_examen']}",
                    f"  Bilan: {exam['bilan']}"
                ])

        return "\n".join(s for s in resume_sections if s)           