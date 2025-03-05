from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    SPECIALTIES = [
        ('GP', 'General Practitioner'),
        ('DENT', 'Dentist'),
        ('CARD', 'Cardiologist'),
        ('OPTH', 'Ophthalmologist'),
        ('ENT', 'ENT Specialist'),
        ('ORTHO', 'Orthopedic'),
        ('NEURO', 'Neurologist'),
        ('DERM', 'Dermatologist'),
        ('PEDIA', 'Pediatrician'),
        ('PSYCH', 'Psychiatrist'),
        ('ONC','Oncologist'),
    ]

    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    specialty = models.CharField(max_length=20, choices=SPECIALTIES, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profilepic/', null=True, blank=True)
    address_line1 = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    google_calendar_authenticated = models.BooleanField(default=False)
    google_calendar_credentials = models.BinaryField(null=True, blank=True)

