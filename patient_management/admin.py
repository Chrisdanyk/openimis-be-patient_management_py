from django.contrib import admin

from patient_management.models import Patient, MedicalRecord

admin.site.register(Patient)
admin.site.register(MedicalRecord)
