"""
URL configuration for Gestion_DPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from authentification.views import AuthenticationViewSet
from Med_Patient.views import PersonnelAdministratifViewSet
from Med_Patient.views import PatientDossierViewSet
from authentification.views import RegisterView
from Med_Patient.views import ConsultationViewSet

schema_view = get_schema_view(
   openapi.Info(
      title="Gestion DPI",
      default_version='v1',
      description="API consacrée à la gestion du DPI des patients",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@votreapi.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


router = DefaultRouter()
router.register(r'auth', AuthenticationViewSet, basename='authentification')
router.register(r'personnel', PersonnelAdministratifViewSet, basename='personnel')
router.register(r'mon-dossier', PatientDossierViewSet, basename='patient-dossier')
router.register(r'Consultation', PatientDossierViewSet, basename='consultation')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Obtenir les tokens
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Rafraîchir le token
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),    # Vérifier le token
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
