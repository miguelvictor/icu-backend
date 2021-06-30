from rest_framework import serializers

from .models import Patient


class PatientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "subject_id",
            "national_id",
            "name",
            "gender",
            "date_of_birth",
            "ethnicity",
            "email",
            "contact_no",
            "address",
            "dod",
        ]
