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
        ('Laborantain', 'Laborantain'),
        ('Radiologue', 'Radiologue'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="laborantain_radiologue")
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
    laborantin_radiologue = models.OneToOneField(
        LaborantinRadiologue,
        on_delete=models.PROTECT,  # Empêche la suppression du laborantin si des résultats existent
        related_name='resultats_examens'
    )

    # Paramètres et leurs valeurs
    glycemie = models.CharField(
        max_length=10,
        verbose_name="glycemie"
    )
    hypertension = models.CharField(
        max_length=10,
        verbose_name="hypertension"
    )

    fer = models.CharField(
        max_length=10,
        verbose_name="fer"
    )
    TSH = models.CharField(
        max_length=10,
        verbose_name="TSH"
    )

    cholesterol = models.CharField(
        max_length=10,
        verbose_name="cholesterol"
    )
    
    # Compte rendu
    compte_rendu = models.TextField(
        verbose_name="Compte rendu",
        null=False,
        blank=False,  # Rend le champ obligatoire
        help_text="Compte rendu détaillé de l'examen"
    )

    # Image médicale
    image_medicale = models.ImageField(
        upload_to='examens/images/',
        validators=[validate_medical_image],
        null=False,
        blank=False,  # Rend le champ obligatoire
        verbose_name="Image médicale",
        help_text="Image médicale au format JPG, PNG ou DICOM"
    )