from django.contrib import admin
from django.urls import path
from django.utils.translation import ugettext_lazy as _

admin.site.site_header = _("ICU Monitoring System")

urlpatterns = [
    path("admin/", admin.site.urls),
]
