from django.db import models
from django.core.exceptions import ValidationError
from authentification.models import User

class Infirmier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="infirmier")
    telephone = models.CharField(max_length=15)

    def __str__(self):
        return f"Infirmier: {self.user.get_full_name()}"

class Pharmacien(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="pharmacien")
    telephone = models.CharField(max_length=15)

    def __str__(self):
        return f"Pharmacien: {self.user.get_full_name()}"

class LaborantinRadiologue(models.Model):
    ROLE_CHOICES = [
        ('Laborantin', 'Laborantin'),
        ('Radiologue', 'Radiologue'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="laborantin_radiologue")
    telephone = models.CharField(max_length=15)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.role}: {self.user.get_full_name()}"
    
class Soin(models.Model):
    
    dossier_patient = models.ForeignKey('Med_Patient.DossierPatient', on_delete=models.CASCADE, related_name="soins")
    infirmier = models.ForeignKey(Infirmier, on_delete=models.CASCADE, related_name="soins", null=True, blank=True)
    date_soin = models.DateField()
    description = models.TextField(null=True, blank=True)
    observation = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"Soin de {self.dossier_patient} - {self.date_soin}"    

def validate_medical_image(value):
    # Liste des extensions autorisées
    valid_extensions = ['.jpg', '.jpeg', '.png', '.dcm']  # dcm pour format DICOM
    ext = str(value.name).lower()[-4:]
    if not any(ext.endswith(valid_ext) for valid_ext in valid_extensions):
        raise ValidationError('Format de fichier non supporté. Utilisez JPG, PNG ou DICOM.')

class ResultatExamen(models.Model):
    # Relations
    examen = models.OneToOneField(
        'Med_Patient.Examen',
        on_delete=models.CASCADE,
        related_name='resultat'
    )
    laborantin_radiologue = models.ForeignKey(LaborantinRadiologue, on_delete=models.CASCADE)
    
    # Paramètres et leurs valeurs
    glycemie = models.CharField(
        max_length=10,
        verbose_name="glycemie",
        null=True
    )
    hypertension = models.CharField(
        max_length=10,
        verbose_name="hypertension",
        null=True
    )

    fer = models.CharField(
        max_length=10,
        verbose_name="fer",
        null=True
    )
    TSH = models.CharField(
        max_length=10,
        verbose_name="TSH",
        null=True
    )

    cholesterol = models.CharField(
        max_length=10,
        verbose_name="cholesterol",
        null=True
    )
    
    # Compte rendu
    compte_rendu = models.TextField(
        verbose_name="Compte rendu",
        null=True,
        blank=True,
        help_text="Compte rendu détaillé de l'examen"
    )

    # Image médicale
    image_medicale = models.ImageField(
        upload_to='examens/images/',
        validators=[validate_medical_image],
        null=True,
        blank=True,
        verbose_name="Image médicale",
        help_text="Image médicale au format JPG, PNG ou DICOM"
    )