from rest_framework import permissions


class IsPersonnelAdministratif(permissions.BasePermission):
    """
    Permission personnalisée qui permet d'accéder à la vue seulement si l'utilisateur a le rôle 'Personnel Administratif'.
    """

    def has_permission(self, request, view):
        # Vérifier si l'utilisateur est authentifié et a le rôle 'Personnel Administratif'
        return request.user and request.user.is_authenticated and request.user.role == 'PA'