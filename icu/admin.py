from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import AppUser, Patient, Admission, ICUStay, ICUEvent
from .filters import (
    ICUStayDischargedFilter,
    AdmissionDischargedFilter,
    PatientDeadFilter,
)


class AdmissionInline(admin.StackedInline):
    model = Admission
    extra = 0
    ordering = ("admittime",)
    classes = ("collapse",)


class PatientAdmin(admin.ModelAdmin):
    search_fields = ["national_id", "name"]
    list_display = ("national_id", "name", "gender", "age", "is_dead")
    list_filter = ("gender", PatientDeadFilter)
    list_per_page = 20
    readonly_fields = ("gender", "date_of_birth")
    fieldsets = [
        (
            _("Basic Information"),
            {"fields": ["national_id", "name", "ethnicity", "gender", "date_of_birth"]},
        ),
        (_("Contact Information"), {"fields": ["contact_no", "email", "address"]}),
        (_("Other Information"), {"fields": ["dod"]}),
    ]
    inlines = [AdmissionInline]


class AdmissionAdmin(admin.ModelAdmin):
    list_display = (
        "hadm_id",
        "get_patient_name",
        "admittime",
        "is_already_discharged",
        "is_dead",
    )
    list_filter = ("admittime", AdmissionDischargedFilter)
    list_per_page = 20
    readonly_fields = ("admittime", "patient")
    fieldsets = (
        (
            _("Patient Information"),
            {
                "fields": [
                    "patient",
                    "insurance",
                    "language",
                    "marital_status",
                ]
            },
        ),
        (
            _("Admission Information"),
            {
                "fields": [
                    "admittime",
                    "admission_type",
                    "admission_location",
                ]
            },
        ),
        (
            _("Discharge Information"),
            {
                "fields": [
                    "dischtime",
                    "discharge_location",
                    "deathtime",
                ]
            },
        ),
        (
            _("ER Department"),
            {"fields": ["edregtime", "edouttime", "hospital_expire_flag"]},
        ),
    )

    def has_add_permission(self, request):
        return False

    def get_patient_name(self, obj):
        return obj.patient.name

    get_patient_name.admin_order_field = "patient"
    get_patient_name.short_description = _("Patient Name")


class ICUStayAdmin(admin.ModelAdmin):
    list_display = (
        "stay_id",
        "get_patient_name",
        "intime",
        "los",
        "is_already_discharged",
    )
    list_filter = ("intime", ICUStayDischargedFilter)
    list_per_page = 20
    readonly_fields = ("intime", "patient", "admission")
    fieldsets = (
        (None, {"fields": ["patient", "admission", "first_careunit", "last_careunit"]}),
        (_("ICU Hospitalization Time"), {"fields": ["intime", "outtime"]}),
    )

    def has_add_permission(self, request):
        return False

    def get_patient_name(self, obj):
        return obj.patient.name

    get_patient_name.admin_order_field = "patient"
    get_patient_name.short_description = _("Patient Name")


class ICUEventAdmin(admin.ModelAdmin):
    search_fields = ("itemid", "label", "abbreviation", "category")
    list_display = ("itemid", "label", "category")
    list_filter = ("linksto",)
    list_per_page = 20
    readonly_fields = ("itemid",)
    fieldsets = (
        (
            _("Basic Information"),
            {"fields": ["itemid", "category", "label", "abbreviation", "unitname"]},
        ),
        (
            _("More Information"),
            {"fields": ["linksto", "param_type", "lownormalvalue", "highnormalvalue"]},
        ),
    )


admin.site.register(AppUser, UserAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Admission, AdmissionAdmin)
admin.site.register(ICUStay, ICUStayAdmin)
admin.site.register(ICUEvent, ICUEventAdmin)
