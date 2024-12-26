from django.db import models
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

class LaborantainRadiologue(models.Model):
    ROLE_CHOICES = [
        ('Laborantain', 'Laborantain'),
        ('Radiologue', 'Radiologue'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="laborantain_radiologue")
    telephone = models.CharField(max_length=15)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.role}: {self.user.get_full_name()}"
