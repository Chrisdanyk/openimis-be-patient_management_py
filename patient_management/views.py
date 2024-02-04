from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics

from patient_management.models import Patient, MedicalRecord
from patient_management.pagination import CustomPageNumberPagination
from patient_management.serializers import (
    PatientSerializer, MedicalRecordSerializer, PatientWithRecordSerializer, )
from rest_framework import response, status, filters
from django_filters.rest_framework import DjangoFilterBackend


class PatientAPIView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_fields = ['id', 'first_name', 'last_name']
    search_fields = ['id', 'first_name', 'last_name']
    ordering_fields = ['id', 'first_name', 'last_name']
    pagination_class = CustomPageNumberPagination

    def perform_create(self, serializer):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(self.request)
        patient = serializer.save()
        return patient

    def get_queryset(self):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(self.request)
        self.serializer_class = PatientWithRecordSerializer
        return super().get_queryset()


class GetUpdateDeletePatientView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        patient = Patient.objects.filter(id=self.kwargs["id"]).first()
        if not patient:
            return response.Response(
                {
                    "error": "Patient not Found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = PatientWithRecordSerializer(patient)
        return response.Response(
            {"message": "success",
             "data": serializer.data},
            status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated, IsAdminUser]
        self.check_permissions(request)
        patient = Patient.objects.filter(id=self.kwargs["id"]).first()
        if not patient:
            return response.Response(
                {
                    "error": "Patient not Found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        patient.delete()
        return response.Response({"message": "Patient deleted successfuly"},
                                 status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated, IsAdminUser]
        self.check_permissions(request)
        patient = Patient.objects.filter(id=self.kwargs["id"]).first()
        if not patient:
            return response.Response(
                {
                    "error": "Patient not Found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(
            patient, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return response.Response(
            {
                "message": "Patient updated successfuly",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


class AddPatientMedicalRecordView(generics.CreateAPIView):
    serializer_class = MedicalRecordSerializer

    def perform_create(self, serializer):
        self.permission_classes = [IsAuthenticated, IsAdminUser]
        self.check_permissions(self.request)
        record = serializer.save(patient_id=self.kwargs['id'])
        return record


class UpdatePatientMedicalRecordView(generics.UpdateAPIView):
    serializer_class = MedicalRecordSerializer
    lookup_field = 'record_id'

    def put(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated, IsAdminUser]
        self.check_permissions(request)
        record = MedicalRecord.objects.filter(
            patient=self.kwargs["id"],
            id=self.kwargs["record_id"]).first()
        if not record:
            return response.Response(
                {
                    "error": "Record not Found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(
            record, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return response.Response(
            {
                "message": "Record updated successfuly",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


class DeletePatientMedicalRecordView(generics.DestroyAPIView):
    serializer_class = MedicalRecordSerializer
    lookup_field = 'record_id'

    def delete(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated, IsAdminUser]
        self.check_permissions(request)
        record = MedicalRecord.objects.filter(
            patient=self.kwargs["id"],
            id=self.kwargs["record_id"]).first()
        if not record:
            return response.Response(
                {
                    "error": "Record not Found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        record.delete()
        return response.Response({"message": "Record deleted successfuly"},
                                 status=status.HTTP_200_OK)
