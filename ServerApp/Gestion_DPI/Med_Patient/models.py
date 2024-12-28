from django.db import models
from Soins_Exams_Patient.models import Soin
from authentification.models import User

class PersonnelAdministratif(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    poste = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.poste}"
    def get_nom(self):
        return f"{self.user.last_name}"
    def get_prenom(self):
        return f"{self.user.first_name} "
    
class Medecin(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

    CARDIOLOGIE = 'Cardiologie'
    DERMATOLOGIE = 'Dermatologie'
    PEDIATRIE = 'Pédiatrie'
    ORTHOPEDIE = 'Orthopédie'
    PSYCHIATRIE = 'Psychiatrie'
    GYNECOLOGIE = 'Gynécologie'

    SPECIALITES_CHOICES = [
        (CARDIOLOGIE, 'Cardiologie'),
        (DERMATOLOGIE, 'Dermatologie'),
        (PEDIATRIE, 'Pédiatrie'),
        (ORTHOPEDIE, 'Orthopédie'),
        (PSYCHIATRIE, 'Psychiatrie'),
        (GYNECOLOGIE, 'Gynécologie'),
    ]
    
    specialite = models.CharField(
        max_length=30,
        choices=SPECIALITES_CHOICES,
        default=CARDIOLOGIE  # Par défaut, choisir "Cardiologie"
    )

    numero_telephone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.specialite}"
    def get_nom(self):
        return f"{self.user.last_name}"
    def get_prenom(self):
        return f"{self.user.first_name} "

class Patient(models.Model):

    # Numéro de sécurité sociale comme clé primaire
    numero_securite_sociale = models.CharField(max_length=15, primary_key=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    date_naissance = models.DateField()
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    mutuelle = models.CharField(max_length=255, blank=True, null=True)
    
    # Lien vers le médecin traitant
    medecin_traitant = models.ForeignKey(Medecin, on_delete=models.SET_NULL, null=True, blank=True)

    # Personne à contacter
    personne_contact_nom = models.CharField(max_length=255, blank=True, null=True)
    personne_contact_telephone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.numero_securite_sociale}"
    def get_username(self):
        return f"{self.user.username}"
    def get_nom(self):
        return f"{self.user.last_name}"
    def get_prenom(self):
        return f"{self.user.first_name} "
    
class DossierPatient(models.Model):

    # Relation 1 à 1 avec le modèle Patient via le NSS
    NSS = models.OneToOneField(Patient, on_delete=models.CASCADE, unique=True)
    
    # Date de dernière mise à jour du dossier
    date_derniere_mise_a_jour = models.DateField(auto_now=True)

    #Les antécédants du patient
    antecedents = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Dossier de {self.NSS.get_nom()} {self.NSS.get_prenom()} - Dernière mise à jour: {self.date_derniere_mise_a_jour}"
    
class Consultation(models.Model):

    # Clé étrangère vers DossierPatient
    dossier_patient = models.ForeignKey(DossierPatient, on_delete=models.CASCADE, related_name="consultations")

    # Clé étrangère vers Medecin
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE, related_name="consultations", null=True, blank=True)
    
    # Date de la consultation
    date_consultation = models.DateField()
    
    # Diagnostic de la consultation
    diagnostic = models.TextField(null=True, blank=True)
    
    # Résumé obligatoire contenant les antécédents
    resume = models.TextField(null=False, blank=False)

class Ordonnance(models.Model):

    # Relation 1 à 1 avec la consultation
    consultation = models.OneToOneField(
        Consultation, 
        on_delete=models.CASCADE, 
        related_name="ordonnance"
    )

    description = models.TextField(null=True, blank=True)
    
    # Date de l'ordonnance
    date_ordonnance = models.DateField(auto_now_add=True)

    # Statut de validation de l'ordonnance
    est_validee = models.BooleanField(
        default=False,
        verbose_name="Ordonnance validée",
        help_text="Indique si l'ordonnance a été validée par le médecin"
    )

class Medicament(models.Model):
    # Nom du médicament
    nom = models.CharField(max_length=255)
    
    # Description facultative du médicament
    description = models.TextField(null=True, blank=True)

    soin = models.ForeignKey(
        Soin,
        on_delete=models.SET_NULL,  # Si un soin est supprimé, l'ID du soin sera mis à NULL
        null=True,
        blank=True,
        related_name="medicaments"
    )

    def __str__(self):
        return self.nom    

class MedicamentOrdonnance(models.Model):
    # Relation avec le médicament
    medicament = models.ForeignKey(
        Medicament,
        on_delete=models.CASCADE,
        related_name="medicament_ordonnances"
    )
    
    # Relation avec l'ordonnance
    ordonnance = models.ForeignKey(
        Ordonnance,
        on_delete=models.CASCADE,
        related_name="medicament_ordonnances"
    )
    
    # Informations supplémentaires
    dose = models.CharField(max_length=50)
    frequence = models.CharField(max_length=50) 
    duree = models.CharField(max_length=50) 

    def __str__(self):
        return (
            f"{self.medicament.nom} - {self.dose}, {self.frequence} pendant {self.duree}"
        )
    
class Examen(models.Model):

    # Relation avec la consultation
    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.CASCADE,
        related_name="examens"
    )
    
    # Types d'examen
    TYPE_EXAMEN_CHOICES = [
        ('biologique', 'Biologique'),
        ('radiologique', 'Radiologique'),
    ]
    type_examen = models.CharField(
        max_length=20,
        choices=TYPE_EXAMEN_CHOICES
    )
    
    # Date de l'examen
    date_examen = models.DateField()
    
    # Bilan de l'examen
    bilan = models.TextField(null=True, blank=True)
