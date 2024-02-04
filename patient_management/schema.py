import graphene
from core import ExtendedConnection
from core.schema import OrderedDjangoFilterConnectionField, OpenIMISMutation
from graphene_django import DjangoObjectType

from patient_management.models import Patient, MedicalRecord


class PatientGQLType(DjangoObjectType):
    """
    Patient Model ENtity
    """
    class Meta:
        model = Patient
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "first_name": ["exact", "istartswith", "icontains", "iexact"],
            "last_name": ["exact", "istartswith", "icontains", "iexact"],
            "telephone": ["exact", "istartswith", "icontains", "iexact"],
            "email": ["exact", "istartswith", "icontains", "iexact"],
            "address": ["exact", "istartswith", "icontains", "iexact"],
            "date_of_birth": ["exact", "lt", "lte", "gt", "gte"],
            "insurance_number": [
                "exact", "istartswith", "icontains", "iexact"],
        }
        connection_class = ExtendedConnection


class MedicalRecordGQLType(DjangoObjectType):
    """
    """
    class Meta:
        model = MedicalRecord
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "patient": ["exact"],
            "hospital": ["exact"],
            "symptoms": ["contains"],
            "diagnosis": ["contains"],
        }
        connection_class = ExtendedConnection


class Query(graphene.ObjectType):
    patients = OrderedDjangoFilterConnectionField(
        PatientGQLType,
        orderBy=graphene.List(of_type=graphene.String)
    )
    medical_records = OrderedDjangoFilterConnectionField(
        MedicalRecordGQLType,
        orderBy=graphene.List(of_type=graphene.String)
    )


class CreatePatientInputType(OpenIMISMutation.Input):

    first_name = graphene.String(required=True, max_length=100)
    last_name = graphene.String(required=True, max_length=100)
    telephone = graphene.String(max_length=13)
    email = graphene.String()
    address = graphene.String(max_length=100)
    date_of_birth = graphene.Date()
    gender = graphene.String()
    insurance_number = graphene.String(max_length=30)


class CreatePatientMutation(OpenIMISMutation):
    _mutation_module = "patient_management"
    _mutation_class = "CreatePatientMutation"

    class Input(CreatePatientInputType):
        pass

    @classmethod
    def async_mutate(cls, user, **data):
        Patient.objects.create(**data)


class PatientInput(graphene.InputObjectType):

    first_name = graphene.String(required=True, max_length=100)
    last_name = graphene.String(required=True, max_length=100)
    telephone = graphene.String(max_length=13)
    email = graphene.String()
    address = graphene.String(max_length=100)
    date_of_birth = graphene.Date()
    gender = graphene.String()
    insurance_number = graphene.String(max_length=30)


class CreateMedicalRecordInputType(OpenIMISMutation.Input):
    patient = graphene.Field(PatientInput)
    symptoms = graphene.String()
    diagnosis = graphene.String()
    hospital = graphene.String(max_length=50, required=True)


class CreateMedicalRecordMutation(OpenIMISMutation):
    _mutation_module = "patient_management"
    _mutation_class = "CreateMedicalRecordMutation"

    class Input(CreateMedicalRecordInputType):
        pass

    @classmethod
    def async_mutate(cls, user, **data):
        MedicalRecord.objects.create(**data)


class Mutation(graphene.ObjectType):
    create_patient = CreatePatientMutation.Field()
    create_medical_record = CreateMedicalRecordMutation.Field()
