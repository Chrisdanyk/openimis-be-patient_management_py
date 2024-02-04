from django.db import models
from django.utils.translation import gettext_lazy as _

from patient_management.model import SoftDeleteModel


class Patient(SoftDeleteModel):
    class Gender(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    telephone = models.CharField(null=True, blank=True, max_length=13)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=2,
        choices=Gender.choices,
        default=Gender.MALE
    )
    insurance_number = models.CharField(null=True, blank=True, max_length=30)


class MedicalRecord(SoftDeleteModel):

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    symptoms = models.TextField(null=True, blank=True)
    diagnosis = models.TextField(null=True, blank=True)
    hospital = models.CharField(max_length=50, null=True, blank=True)
