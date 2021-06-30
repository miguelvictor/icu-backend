from django.contrib import admin
from django.urls import path, include
from django.utils.translation import ugettext_lazy as _

admin.site.site_header = _("ICU Monitoring System")

urlpatterns = [
    path("api/v1/", include("icu.urls")),
    path("admin/", admin.site.urls),
]
