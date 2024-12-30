from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from Soins_Exams_Patient.models import ResultatExamen
from .serializers import ExamenSerializer, OrdonnancePharmacienSerializer, ResultatExamenSerializer
from .permissions import IsLaborantinRadiologueUser, IsPharmacientUser
from django.shortcuts import get_object_or_404
from Med_Patient.models import Examen, Ordonnance
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class PharmacienViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsPharmacientUser]
    serializer_class = OrdonnancePharmacienSerializer
    
    @swagger_auto_schema(
        operation_description="Valide ou dévalide une ordonnance spécifique",
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="ID de l'ordonnance",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['action'],
            properties={
                'action': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['valider', 'devalider'],
                    description="Action à effectuer : 'valider' pour valider ou 'devalider' pour dévalider"
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Ordonnance validée ou dévalidée avec succès",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Message de confirmation de l'action"
                        ),
                        'data': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            additional_properties=openapi.Schema(
                                type=openapi.TYPE_STRING
                            )
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Action invalide. L'action doit être 'valider' ou 'devalider'."
            ),
            404: openapi.Response(
                description="Ordonnance non trouvée"
            ),
            403: openapi.Response(
                description="Accès non autorisé - L'utilisateur n'est pas un pharmacien"
            )
        },
        operation_id='valider_ordonnance'
    )

    @action(detail=True, methods=['post'])
    def valider_ordonnance(self, request, pk=None):
        """
        Endpoint pour valider ou dévalider une ordonnance selon l'action demandée
        """
        ordonnance = get_object_or_404(Ordonnance, pk=pk)
        action = request.data.get('action')
        
        if action not in ['valider', 'devalider']:
            return Response(
                {"error": "L'action doit être 'valider' ou 'devalider'"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Mise à jour selon l'action
        ordonnance.est_validee = (action == 'valider')
        ordonnance.save()
        
        serializer = self.serializer_class(ordonnance)
        return Response({
            'message': f"Ordonnance {'validée' if action == 'valider' else 'dévalidée'} avec succès",
            'data': serializer.data
        })

    def list(self, request):
        ordonnances = Ordonnance.objects.all().prefetch_related(
            'medicament_ordonnances__medicament',
            'consultation__dossier_patient__NSS'
        )
        
        serializer = self.serializer_class(ordonnances, many=True)
        return Response(serializer.data)
    
class ResultatExamenViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsLaborantinRadiologueUser]
    serializer_class = ResultatExamenSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        """
        Associe automatiquement le laborantin/radiologue connecté au résultat
        """
        serializer.save(
            laborantin_radiologue=self.request.user.laborantin_radiologue
        )

    def get_queryset(self):
        user = self.request.user
        try:
            laborantin_radiologue = user.laborantin_radiologue
            if laborantin_radiologue.role == 'Laborantin':
                return ResultatExamen.objects.filter(
                    examen__type_examen='biologique'
                )
            else:  # Radiologue
                return ResultatExamen.objects.filter(
                    examen__type_examen='radiologique'
                )
        except:
            return ResultatExamen.objects.none()

    @action(detail=False, methods=['get'])
    def examens_a_traiter(self, request):
        """Récupère les examens qui n'ont pas encore de résultats"""
        user = request.user
        try:
            laborantin_radiologue = user.laborantin_radiologue
            if laborantin_radiologue.role == 'Laborantin':
                examens = Examen.objects.filter(
                    type_examen='biologique',
                    resultat__isnull=True
                )
            else:  # Radiologue
                examens = Examen.objects.filter(
                    type_examen='radiologique',
                    resultat__isnull=True
                )
            
            return Response({
                'examens': ExamenSerializer(examens, many=True).data
            })
        except:
            return Response(
                {"error": "Utilisateur non autorisé"}, 
                status=status.HTTP_403_FORBIDDEN
            )

    @action(detail=False, methods=['get'])
    def resultats_patient(self, request):
        """Récupère tous les résultats d'un patient par son NSS"""
        nss = request.query_params.get('nss')
        if not nss:
            return Response(
                {"error": "NSS requis"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        try:
            laborantin_radiologue = user.laborantin_radiologue
            resultats = ResultatExamen.objects.filter(
                examen__consultation__dossier_patient__NSS__numero_securite_sociale=nss
            )
            
            # Filtrer selon le rôle
            if laborantin_radiologue.role == 'Laborantin':
                resultats = resultats.filter(examen__type_examen='biologique')
            else:  # Radiologue
                resultats = resultats.filter(examen__type_examen='radiologique')
            
            return Response(
                self.get_serializer(resultats, many=True).data
            )
        except:
            return Response(
                {"error": "Utilisateur non autorisé"}, 
                status=status.HTTP_403_FORBIDDEN
            )    
