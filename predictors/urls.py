from django.urls import path

from .views import get_dashboard_info, get_dashboard_graph

urlpatterns = [
    path("dashboard-info/", get_dashboard_info),
    path("dashboard-graph/", get_dashboard_graph),
]
