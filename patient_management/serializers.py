from rest_framework import serializers

from patient_management.models import Patient, MedicalRecord


class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = '__all__'
        readonly = ('id', 'created_at', 'updated_at', 'deleted_at',)

        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'deleted_at': {'read_only': True},
            'patient': {'read_only': True}
        }


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        readonly = ('id', 'created_at', 'updated_at', 'deleted_at',)
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'deleted_at': {'read_only': True}
        }

    def validate(self, data):
        if 'start_date' and 'end_date' in data:
            if data['start_date'] > data['end_date']:
                raise serializers. \
                    ValidationError('The end date should '
                                    'be after the start date')
        return data


class PatientWithRecordSerializer(serializers.ModelSerializer):
    medical_records = MedicalRecordSerializer(
        many=True, read_only=True, source='medicalrecord_set')

    class Meta:
        model = Patient
        fields = '__all__'
        readonly = ('id', 'created_at', 'updated_at', 'deleted_at',)
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'deleted_at': {'read_only': True}
        }

    def validate(self, data):
        if 'start_date' and 'end_date' in data:
            if data['start_date'] > data['end_date']:
                raise serializers. \
                    ValidationError('The end date should '
                                    'be after the start date')
        return data
