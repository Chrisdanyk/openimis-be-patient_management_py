from django.urls import path
from patient_management.views import (
    PatientAPIView, GetUpdateDeletePatientView,
    AddPatientMedicalRecordView, UpdatePatientMedicalRecordView,
    DeletePatientMedicalRecordView)

urlpatterns = [
    path('', PatientAPIView.as_view(), name='patients'),
    path('<int:id>', GetUpdateDeletePatientView.as_view(),
         name='patient'),
    path('<int:id>/add_medical_record',
         AddPatientMedicalRecordView.as_view(),
         name='add_patient_medical_record'),
    path('<int:id>/edit_medical_record/<int:record_id>',
         UpdatePatientMedicalRecordView.as_view(),
         name='edit_patient_medical_record'),
    path('<int:id>/delete_medical_record/<int:record_id>',
         DeletePatientMedicalRecordView.as_view(),
         name='delete_patient_medical_record'),
]
