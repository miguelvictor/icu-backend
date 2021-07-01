from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import AppUser, LabEvent, LabItem, Patient, Admission, ICUStay, ICUEvent
from .filters import (
    ICUStayDischargedFilter,
    AdmissionDischargedFilter,
    PatientDeadFilter,
)


class AppUserAdmin(UserAdmin):
    readonly_fields = ("id", "worker_id", "gender", "date_of_birth", "start_date")
    fieldsets = (
        (None, {"fields": ("id", "worker_id", "username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "national_id",
                    "first_name",
                    "last_name",
                    "gender",
                    "date_of_birth",
                )
            },
        ),
        (
            _("Employment Information"),
            {"fields": ("position", "start_date")},
        ),
        (
            _("Contact Information"),
            {"fields": ("contact_no", "email")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


class AdmissionInline(admin.StackedInline):
    model = Admission
    extra = 0
    ordering = ("admittime",)
    classes = ("collapse",)


class PatientAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            _("Basic Information"),
            {"fields": ["national_id", "name", "ethnicity", "gender", "date_of_birth"]},
        ),
        (_("Contact Information"), {"fields": ["contact_no", "email", "address"]}),
        (_("Other Information"), {"fields": ["dod"]}),
    ]
    inlines = [AdmissionInline]
    list_display = ("national_id", "name", "gender", "age", "is_dead")
    list_filter = ("gender", PatientDeadFilter)
    list_per_page = 20
    readonly_fields = ("gender", "date_of_birth")
    search_fields = ["subject_id", "national_id", "name"]


class AdmissionAdmin(admin.ModelAdmin):
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
    list_display = (
        "hadm_id",
        "get_patient_name",
        "admittime",
        "is_already_discharged",
        "is_dead",
    )
    list_filter = ("admittime", AdmissionDischargedFilter)
    list_per_page = 20
    raw_id_fields = ("patient",)
    readonly_fields = ("admittime",)
    search_fields = ("hadm_id", "patient__national_id", "patient__name")

    def get_patient_name(self, obj):
        return obj.patient.name

    get_patient_name.admin_order_field = "patient"
    get_patient_name.short_description = _("Patient Name")


class ICUStayAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ["patient", "admission", "first_careunit", "last_careunit"]}),
        (_("ICU Hospitalization Time"), {"fields": ["intime", "outtime"]}),
    )
    list_display = (
        "stay_id",
        "get_patient_name",
        "intime",
        "los",
        "is_already_discharged",
    )
    list_filter = ("intime", ICUStayDischargedFilter)
    list_per_page = 20
    readonly_fields = ("intime",)
    raw_id_fields = ("patient", "admission")
    search_fields = (
        "stay_id",
        "patient__national_id",
        "patient__name",
        "admission__hadm_id",
    )

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


class LabItemAdmin(admin.ModelAdmin):
    search_fields = ("itemid", "label", "fluid", "category", "loinc_code")
    list_display = ("itemid", "label", "category")
    list_filter = ("category",)
    list_per_page = 20
    readonly_fields = ("itemid",)
    fields = ("itemid", "label", "category", "fluid", "loinc_code")


class LabEventAdmin(admin.ModelAdmin):
    list_per_page = 20


# Core Module
admin.site.register(AppUser, AppUserAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Admission, AdmissionAdmin)

# ICU Module
admin.site.register(ICUStay, ICUStayAdmin)
admin.site.register(ICUEvent, ICUEventAdmin)

# Hospital Module
admin.site.register(LabItem, LabItemAdmin)
admin.site.register(LabEvent, LabEventAdmin)
