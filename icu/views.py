from rest_framework.viewsets import ModelViewSet

from .models import Patient
from .serializers import PatientSerializer


class PatientsViewSet(ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
