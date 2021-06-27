from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class ICUStayDischargedFilter(admin.SimpleListFilter):
    title = _("Already Discharged in ICU?")
    parameter_name = "already_discharged"

    def lookups(self, request, model_admin):
        return (
            ("Yes", _("Yes")),
            ("No", _("No")),
        )

    def queryset(self, request, queryset):
        value = self.value()

        if value == "Yes":
            return queryset.filter(outtime__isnull=False)

        if value == "No":
            return queryset.filter(outtime__isnull=True)

        return queryset


class AdmissionDischargedFilter(admin.SimpleListFilter):
    title = _("Already Discharged in Hospital?")
    parameter_name = "already_discharged"

    def lookups(self, request, model_admin):
        return (
            ("Yes", _("Yes")),
            ("No", _("No")),
        )

    def queryset(self, request, queryset):
        value = self.value()

        if value == "Yes":
            return queryset.filter(dischtime__isnull=False)

        if value == "No":
            return queryset.filter(dischtime__isnull=True)

        return queryset


class PatientDeadFilter(admin.SimpleListFilter):
    title = _("Patient Died?")
    parameter_name = "patient_died"

    def lookups(self, request, model_admin):
        return (
            ("Yes", _("Yes")),
            ("No", _("No")),
        )

    def queryset(self, request, queryset):
        value = self.value()

        if value == "Yes":
            return queryset.filter(dod__isnull=False)

        if value == "No":
            return queryset.filter(dod__isnull=True)

        return queryset