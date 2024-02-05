from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone

from patient_management.manager import SoftDeleteManager


class SoftDeleteModel(models.Model):
    """
    Base model
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeleteManager()
    all_objects = SoftDeleteManager(alive_only=False)

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super().delete()

    class Meta:
        abstract = True

    @staticmethod
    def concat_values(*args):
        return ''.join(args)


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
