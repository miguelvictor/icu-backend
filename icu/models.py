from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4

from .choices import (
    ADMISSION_TYPE_CHOICES,
    DITEMS_LINKSTO_CHOICES,
    DITEMS_PARAM_TYPE_CHOICES,
    ETHNICITY_CHOICES,
    GENDER_CHOICES,
    MARITAL_STATUS_CHOICES,
    POSITION_CHOICES,
)
from .managers import AppUserManager
from .validators import validate_national_id


class AppUser(AbstractUser):
    national_id = models.CharField(
        _("National ID"),
        max_length=18,
        unique=True,
        validators=[validate_national_id],
    )
    gender = models.CharField(_("gender"), max_length=1, choices=GENDER_CHOICES)
    contact_no = models.CharField(_("Contact Number"), max_length=150, blank=True)
    date_of_birth = models.DateField(_("Date of Birth"), null=True, blank=True)
    worker_id = models.UUIDField(_("worker ID"), unique=True, default=uuid4)
    position = models.CharField(_("position"), max_length=50, choices=POSITION_CHOICES)
    start_date = models.DateField(_("Start Date"), auto_now_add=True)

    objects = AppUserManager()

    def __str__(self):
        return f"{self.username}: {self.email}"


class Patient(models.Model):
    subject_id = models.BigAutoField(_("patient ID"), primary_key=True)
    national_id = models.CharField(
        _("National ID"),
        max_length=18,
        validators=[validate_national_id],
    )
    name = models.CharField(_("Patient Name"), max_length=255)
    gender = models.CharField(
        _("gender"), max_length=1, editable=False, choices=GENDER_CHOICES
    )
    date_of_birth = models.DateField(_("Date of Birth"), editable=False)
    ethnicity = models.CharField(
        _("ethnicity"), max_length=50, choices=ETHNICITY_CHOICES
    )
    email = models.EmailField(_("email"), null=True, blank=True)
    contact_no = models.CharField(
        _("contact number"), max_length=150, null=True, blank=True
    )
    address = models.TextField(_("address"), null=True, blank=True)
    dod = models.DateTimeField(_("Date of Death"), null=True, blank=True)

    @admin.display(ordering="date_of_birth", description=_("age"))
    def age(self):
        now, dob = timezone.now(), self.date_of_birth
        extra = (now.month, now.day) < (dob.month, dob.day)
        return now.year - dob.year - extra

    @admin.display(ordering="dod", description=_("Dead?"), boolean=True)
    def is_dead(self):
        return self.dod != None

    def __str__(self):
        return f"【{self.subject_id}】{self.name}"

    class Meta:
        indexes = [
            models.Index(fields=["national_id"]),
            models.Index(fields=["name"]),
        ]
        verbose_name = _("patient")
        verbose_name_plural = _("patients")


class Admission(models.Model):
    hadm_id = models.BigAutoField(_("Admission ID"), primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    admittime = models.DateTimeField(
        _("Admission Time"),
        auto_now_add=True,
        help_text=_(
            "Provides the date and time the patient was admitted to the hospital."
        ),
    )
    dischtime = models.DateTimeField(
        _("Discharge Time"),
        null=True,
        blank=True,
        help_text=_(
            "Provides the date and time the patient was discharged from the hospital."
        ),
    )
    deathtime = models.DateTimeField(
        _("Death Time"),
        null=True,
        blank=True,
        help_text=_(
            "Provides the time of in-hospital death for the patient. "
            "Note that this is only present if the patient died in-hospital, "
            "and is almost always the same as the dischtime field."
        ),
    )
    admission_type = models.CharField(
        _("Admission Type"),
        max_length=50,
        choices=ADMISSION_TYPE_CHOICES,
        help_text=_("Useful for classifying the urgency of the admission."),
    )
    admission_location = models.CharField(
        _("Admission Location"),
        max_length=60,
        null=True,
        blank=True,
        help_text=_(
            "Provides information about the location of the patient prior to arriving at the hospital. "
            "Note that as the emergency room is technically a clinic, patients who are admitted "
            "via the emergency room usually have it as their admission location."
        ),
    )
    discharge_location = models.CharField(
        _("Discharge Location"),
        max_length=60,
        null=True,
        blank=True,
        help_text=_(
            "The disposition of the patient after they are discharged from the hospital."
        ),
    )
    insurance = models.CharField(_("insurance"), max_length=255, blank=True)
    language = models.CharField(_("language"), max_length=50, blank=True)
    marital_status = models.CharField(
        _("marital status"),
        max_length=50,
        choices=MARITAL_STATUS_CHOICES,
        null=True,
        blank=True,
    )
    edregtime = models.DateTimeField(
        _("ED Registration Time"),
        null=True,
        blank=True,
        help_text=_(
            "The date and time at which the patient was registered from the emergency department."
        ),
    )
    edouttime = models.DateTimeField(
        _("ED Discharge Time"),
        null=True,
        blank=True,
        help_text=_(
            "The date and time at which the patient was discharged from the emergency department."
        ),
    )
    hospital_expire_flag = models.BooleanField(
        _("Hospital Expire Flag"),
        blank=True,
        help_text=_(
            "This is a binary flag which indicates whether the patient died within the given hospitalization. "
            "1 indicates death in the hospital, and 0 indicates survival to hospital discharge."
        ),
    )

    @admin.display(ordering="dischtime", description=_("Discharged?"), boolean=True)
    def is_already_discharged(self):
        return self.dischtime != None

    @admin.display(ordering="deathtime", description=_("Dead?"), boolean=True)
    def is_dead(self):
        return self.deathtime != None

    def __str__(self):
        patient_id = self.patient.subject_id
        name = self.patient.name
        admission_order = (
            self.patient.admission_set.order_by("admittime")
            .filter(admittime__lte=self.admittime)
            .count()
        )

        return f"【{patient_id}】{name}的第 {admission_order} 次入院"

    class Meta:
        indexes = [models.Index(fields=["admittime"])]
        verbose_name = _("admission")
        verbose_name_plural = _("admissions")


class ICUStay(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE)
    stay_id = models.BigAutoField(_("ICU Stay ID"), primary_key=True)
    first_careunit = models.CharField(
        _("First Care Unit"),
        max_length=20,
        help_text=_("The first ICU type in which the patient was cared for."),
    )
    last_careunit = models.CharField(
        _("Last Care Unit"),
        max_length=20,
        help_text=_("The last ICU type in which the patient was cared for."),
    )
    intime = models.DateTimeField(
        _("Time In"),
        auto_now_add=True,
        help_text=_(
            "Provides the date and time the patient was transferred into the ICU."
        ),
    )
    outtime = models.DateTimeField(
        _("Time Out"),
        null=True,
        blank=True,
        help_text=_(
            "Provides the date and time the patient was transferred out of the ICU."
        ),
    )

    @admin.display(ordering="outtime", description=_("ICU Discharged?"), boolean=True)
    def is_already_discharged(self):
        return self.outtime != None

    @admin.display(ordering="intime", description=_("Length of Stay"))
    def los(self):
        delta = timezone.now() - self.intime
        return delta.days

    def __str__(self):
        patient_id = self.patient.subject_id
        name = self.patient.name
        admission_order = (
            self.patient.admission_set.order_by("admittime")
            .filter(admittime__lte=self.admission.admittime)
            .count()
        )
        icu_stay_order = (
            self.admission.icustay_set.order_by("intime")
            .filter(intime__lte=self.intime)
            .count()
        )

        return f"【{patient_id}】{name}的第 {admission_order} 次入院的第 {icu_stay_order} 个 ICU stay"

    class Meta:
        verbose_name = _("ICU stay")
        verbose_name_plural = _("ICU stays")


class ICUEvent(models.Model):
    itemid = models.AutoField(_("Item ID"), primary_key=True)
    label = models.CharField(
        _("label"),
        max_length=200,
        help_text=_("Describes the concept which is represented by this item."),
    )
    abbreviation = models.CharField(
        _("abbreviation"),
        max_length=100,
        help_text=_("Lists a common abbreviation for the label."),
    )
    linksto = models.CharField(
        _("Links To"),
        max_length=50,
        choices=DITEMS_LINKSTO_CHOICES,
        help_text=_(
            "Provides the table name which the data links to. "
            "For example, a value of ‘chartevents’ indicates that the itemid "
            "of the given row is contained in the CHARTEVENTS table. A single itemid is only used "
            "in one event table, that is, if an itemid is contained in CHARTEVENTS "
            "it will not be contained in any other event table (e.g. IOEVENTS, CHARTEVENTS, etc)."
        ),
    )
    category = models.CharField(
        _("category"),
        max_length=100,
        help_text=_(
            "Provides some information of the type of data the itemid corresponds to. "
            "Examples include ‘ABG’, which indicates the measurement is sourced "
            "from an arterial blood gas, ‘IV Medication’, which indicates that the medication "
            "is administered through an intravenous line, and so on."
        ),
    )
    unitname = models.CharField(
        _("Unit Name"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_(
            "Specifies the unit of measurement used for the itemid. "
            "This column is not always available, and this may be because "
            "the unit of measurement varies, a unit of measurement does not make sense "
            "for the given data type, or the unit of measurement is simply missing. "
            "Note that there is sometimes additional information on the unit of measurement "
            "in the associated event table, e.g. the valueuom column in CHARTEVENTS."
        ),
    )
    param_type = models.CharField(
        _("Parameter Type"),
        max_length=30,
        choices=DITEMS_PARAM_TYPE_CHOICES,
        help_text=_(
            "Describes the type of data which is recorded: a date, a number or a text field."
        ),
    )
    lownormalvalue = models.FloatField(
        _("Low Normal Value"),
        null=True,
        blank=True,
        help_text=_(
            "Stores the lowest but still considered normal value for the this measurement."
        ),
    )
    highnormalvalue = models.FloatField(
        _("High Normal Value"),
        null=True,
        blank=True,
        help_text=(
            "Stores the highest but still considered normal value for the this measurement. "
            "Note that a reference range encompasses the expected value of a measurement: "
            "values outside of this may still be physiologically plausible, but are considered unusual."
        ),
    )

    def __str__(self):
        return f"#{self.itemid}【{self.category}】{self.label }"

    class Meta:
        verbose_name = _("ICU Event")
        verbose_name_plural = _("ICU Events")


class ChartEvent(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE)
    icustay = models.ForeignKey(ICUStay, on_delete=models.CASCADE)
    charttime = models.DateTimeField(
        _("chart time"),
        help_text=_(
            "Records the time at which an observation was made, "
            "and is usually the closest proxy to the time the data was actually measured."
        ),
    )
    storetime = models.DateTimeField(
        _("store time"),
        help_text=_(
            "Records the time at which an observation was manually input or "
            "manually validated by a member of the clinical staff."
        ),
    )
    icuevent = models.ForeignKey(ICUEvent, on_delete=models.CASCADE)
    value = models.TextField(
        _("value"),
        help_text=_(
            "Contains the value measured for the concept identified by the ITEMID."
        ),
    )
    valuenum = models.FloatField(
        _("value (numeric)"),
        blank=True,
        help_text=_(
            "The numeric format of the same value. "
            "If data is not numeric, this field is null."
        ),
    )
    valueuom = models.TextField(
        _("unit of measurement"),
        blank=True,
        help_text=_("The unit of measurement for the value, if appropriate."),
    )
    warning = models.BooleanField(
        _("warning"),
        help_text=_(
            "Specifies if a warning for this observation was "
            "manually documented by the care provider."
        ),
    )

    class Meta:
        verbose_name = _("chart event")
        verbose_name_plural = _("chart events")


class LabItem(models.Model):
    itemid = models.AutoField(
        _("Item ID"),
        primary_key=True,
        help_text=_(
            "A unique identifier for a laboratory concept. "
            "itemid is unique to each row, and can be used "
            "to identify data in LABEVENTS associated with a specific concept."
        ),
    )
    label = models.CharField(
        _("Label"),
        max_length=50,
        help_text=_("Describes the concept which is represented by the itemid."),
    )
    fluid = models.CharField(
        _("Fluid"),
        max_length=50,
        help_text=_(
            "Describes the substance on which the measurement was made. "
            "For example, chemistry measurements are frequently performed on blood, "
            "which is listed in this column as ‘BLOOD’. Many of these measurements "
            "are also acquirable on other fluids, such as urine, and this column "
            "differentiates these distinct concepts."
        ),
    )
    category = models.CharField(
        _("category"),
        max_length=50,
        help_text=_(
            "Provides higher level information as to the type of measurement. "
            "For example, a category of ‘ABG’ indicates that the measurement is an arterial blood gas."
        ),
    )
    loinc_code = models.CharField(
        _("LOINC Code"),
        max_length=50,
        blank=True,
        help_text=_(
            "Contains the LOINC code associated with the given itemid. "
            "LOINC is an ontology which originally specified laboratory measurements "
            "but has since expanded to cover a wide range of clinically relevant concepts. "
            "LOINC openly provide a table which contains a large amount of detail about each LOINC code. "
            "This table is freely available online."
        ),
    )

    def __str__(self):
        return f"【{self.itemid}】{self.label}"

    class Meta:
        verbose_name = _("Laboratory Item")
        verbose_name_plural = _("Laboratory Items")


class LabEvent(models.Model):
    labevent_id = models.AutoField(_("Lab Event ID"), primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE)
    specimen_id = models.IntegerField(
        _("Specimen ID"),
        help_text=_(
            "Uniquely denoted the specimen from which the lab measurement was made. "
            "Most lab measurements are made on patient derived samples (specimens) such as blood, "
            "urine, and so on. Often multiple measurements are made on the same sample. "
            "The specimen_id will group measurements made on the same sample, "
            "e.g. blood gas measurements made on the same sample of blood."
        ),
    )
    lab_item = models.ForeignKey(LabItem, on_delete=models.CASCADE)
    charttime = models.DateTimeField(
        _("Chart Time"),
        help_text=_(
            "The time at which the laboratory measurement was charted. "
            "This is usually the time at which the specimen was acquired, "
            "and is usually significantly earlier than the time at which the measurement is available."
        ),
    )
    storetime = models.DateTimeField(
        _("Store Time"),
        null=True,
        blank=True,
        help_text=_(
            "The time at which the measurement was made available in the laboratory system. "
            "This is when the information would have been available to care providers."
        ),
    )
    value = models.CharField(
        _("value"),
        max_length=200,
        help_text=_("The result of the laboratory measurement."),
    )
    valuenum = models.FloatField(
        _("Value (Numeric)"),
        null=True,
        blank=True,
        help_text=_(
            "If value is numeric, this contains the value cast as a numeric data type."
        ),
    )
    valueuom = models.CharField(
        _("Unit of Measurement"),
        max_length=20,
        blank=True,
        help_text=_("The unit of measurement for the laboratory concept."),
    )
    ref_range_lower = models.FloatField(
        _("Ref Range Lower"),
        null=True,
        blank=True,
        help_text=_(
            "Lower reference range indicating the normal range for the laboratory measurements. Values outside the reference ranges are considered abnormal."
        ),
    )
    ref_range_upper = models.FloatField(
        _("Ref Range Upper"),
        null=True,
        blank=True,
        help_text=_(
            "Upper reference range indicating the normal range for the laboratory measurements. Values outside the reference ranges are considered abnormal."
        ),
    )
    flag = models.CharField(
        _("Flag"),
        max_length=10,
        blank=True,
        help_text=_(
            "A brief string mainly used to indicate if the laboratory measurement is abnormal."
        ),
    )
    priority = models.CharField(
        _("Priority"),
        max_length=7,
        blank=True,
        help_text=_(
            "The priority of the laboratory measurement: either routine or stat (urgent)."
        ),
    )
    comments = models.TextField(
        _("Comments"),
        blank=True,
        help_text=_(
            "Deidentified free-text comments associated with the laboratory measurement. "
            "Usually these provide information about the sample, whether any notifications "
            "were made to care providers regarding the results, considerations for interpretation, "
            "or in some cases the comments contain the result of the laboratory itself. "
            "Comments which have been fully deidentified (i.e. no information content retained) "
            "are present as three underscores: ___. A NULL comment indicates no comment was made for the row."
        ),
    )

    class Meta:
        verbose_name = _("Laboratory Event")
        verbose_name_plural = _("Laboratory Events")
