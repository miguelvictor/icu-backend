from datetime import datetime
from rest_framework import serializers

from .models import AppUser, Patient


class PatientSerializer(serializers.HyperlinkedModelSerializer):
    gender = serializers.SerializerMethodField()
    ethnicity = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()

    def get_gender(self, obj):
        return obj.get_gender_display()

    def get_ethnicity(self, obj):
        return obj.get_ethnicity_display()

    def get_age(self, obj):
        bday = obj.date_of_birth
        now = datetime.now()
        return now.year - bday.year - ((now.month, now.day) < (bday.month, bday.day))

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
            "age",
        ]


class DoctorSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()

    def get_name(self, obj):
        return f"{obj.last_name}{obj.first_name}"

    def get_gender(self, obj):
        return obj.get_gender_display()

    def get_position(self, obj):
        return obj.get_position_display()

    class Meta:
        model = AppUser
        fields = [
            "id",
            "national_id",
            "gender",
            "contact_no",
            "date_of_birth",
            "worker_id",
            "position",
            "start_date",
            "email",
            "name",
            "is_active",
        ]
