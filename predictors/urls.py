from django.urls import path

from .views import get_dashboard_info, get_dashboard_graph, get_dashboard_patients

urlpatterns = [
    path("dashboard-info/", get_dashboard_info),
    path("dashboard-graph/", get_dashboard_graph),
    path("dashboard-patients/", get_dashboard_patients),
]
