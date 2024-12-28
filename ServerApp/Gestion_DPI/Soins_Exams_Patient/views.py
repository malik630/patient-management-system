from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import OrdonnancePharmacienSerializer
from .permissions import IsPharmacientUser
from django.shortcuts import get_object_or_404

from Med_Patient.models import Ordonnance

class PharmacienViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsPharmacientUser]
    serializer_class = OrdonnancePharmacienSerializer
    
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