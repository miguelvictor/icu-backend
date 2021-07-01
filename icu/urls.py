from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import DoctorsViewSet, PatientsViewSet

router = DefaultRouter()
router.register(r"patients", PatientsViewSet)
router.register(r"doctors", DoctorsViewSet)


urlpatterns = [
    path("jwt-token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("jwt-token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
