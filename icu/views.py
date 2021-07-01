from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from .models import Patient, AppUser
from .serializers import DoctorSerializer, PatientSerializer


class PatientsViewSet(ReadOnlyModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class DoctorsViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    queryset = AppUser.objects.all()
    serializer_class = DoctorSerializer

    def perform_update(self, serializer):
        if self.request.user.id != serializer.id:
            raise PermissionDenied()

        return super().perform_update(serializer)
