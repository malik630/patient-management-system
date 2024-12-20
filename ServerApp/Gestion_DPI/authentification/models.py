from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    Role = [
        ('P', 'Patient'),
        ('M', 'Médecin'),
        ('PA', 'Personnel Administratif'),
        ('PH', 'Pharmacien'),
        ('I', 'Infirmier'),
        ('LR', 'Laborantin/Radiologue')
    ]
    
    role = models.CharField(
        max_length=2,
        choices=Role,
        default='P',
        null=False,
        blank=False
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['role', 'password']

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name