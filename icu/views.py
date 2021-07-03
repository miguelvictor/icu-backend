from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Patient, AppUser
from .serializers import DoctorSerializer, PatientSerializer


class PatientsViewSet(ReadOnlyModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class DoctorsViewSet(ReadOnlyModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = DoctorSerializer
