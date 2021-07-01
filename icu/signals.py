from datetime import datetime
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.timezone import get_current_timezone
from django.utils.translation import gettext_lazy as _
from id_validator import validator

from .models import Admission, AppUser, ChartEvent, ICUStay, LabEvent, Patient


@receiver(pre_save, sender=AppUser)
def doctor_pre_save_handler(sender, instance, **kwargs):
    # get info from the patient's national ID
    info = validator.get_info(instance.national_id)
    if info is False:
        raise ValidationError(
            _("%(value)s is not a valid national ID number."),
            params={"value": instance.national_id},
        )

    # patient's gender and date of birth can be retrieved from national ID
    instance.gender = "M" if info["sex"] == 1 else "F"
    instance.date_of_birth = datetime.strptime(info["birthday_code"], r"%Y-%m-%d")


@receiver(pre_save, sender=Patient)
def patient_pre_save_handler(sender, instance, **kwargs):
    # `validator.get_info` is too slow for retrieving information
    # so we only calculate the `date_of_birth` and `gender` of a patient
    # this if clause evaluates only during loading fixtures
    if kwargs.pop("raw", False):
        _id = instance.national_id
        assert type(_id) == str and len(_id) == 18
        gender = "M" if int(_id[-2]) % 2 == 1 else "F"
        date_of_birth = datetime.strptime(_id[6:14], r"%Y%m%d")
        address = None

    # when using the app normally, the national ID input should be
    # validated first before attempting to retrieve information in it
    else:
        # get info from the patient's national ID
        info = validator.get_info(instance.national_id)
        if info is False:
            raise ValidationError(
                _("%(value)s is not a valid national ID number."),
                params={"value": instance.national_id},
            )
        gender = "M" if info["sex"] == 1 else "F"
        date_of_birth = datetime.strptime(info["birthday_code"], r"%Y-%m-%d")
        address = info["address"]

    # patient's gender and date of birth can be retrieved from national ID
    instance.gender = gender
    instance.date_of_birth = date_of_birth

    # a default address can also be added if the instance doesn't have one
    if not instance.address and address is not None:
        instance.address = info["address"]

    # add default timezone to unaware date/time fields
    if instance.dod is not None and instance.dod.tzinfo is None:
        instance.dod = instance.dod.replace(tzinfo=get_current_timezone())


@receiver(pre_save, sender=Admission)
def admission_pre_save_handler(sender, instance, **kwargs):
    # add default timezone to unaware date/time fields
    if instance.admittime is not None and instance.admittime.tzinfo is None:
        instance.admittime = instance.admittime.replace(tzinfo=get_current_timezone())
    if instance.dischtime is not None and instance.dischtime.tzinfo is None:
        instance.dischtime = instance.dischtime.replace(tzinfo=get_current_timezone())
    if instance.deathtime is not None and instance.deathtime.tzinfo is None:
        instance.deathtime = instance.deathtime.replace(tzinfo=get_current_timezone())
    if instance.edregtime is not None and instance.edregtime.tzinfo is None:
        instance.edregtime = instance.edregtime.replace(tzinfo=get_current_timezone())
    if instance.edouttime is not None and instance.edouttime.tzinfo is None:
        instance.edouttime = instance.edouttime.replace(tzinfo=get_current_timezone())


@receiver(pre_save, sender=ICUStay)
def icustay_pre_save_handler(sender, instance, **kwargs):
    # add default timezone to unaware date/time fields
    if instance.intime is not None and instance.intime.tzinfo is None:
        instance.intime = instance.intime.replace(tzinfo=get_current_timezone())
    if instance.outtime is not None and instance.outtime.tzinfo is None:
        instance.outtime = instance.outtime.replace(tzinfo=get_current_timezone())


@receiver(pre_save, sender=LabEvent)
def labevent_pre_save_handler(sender, instance, **kwargs):
    # add default timezone to unaware date/time fields
    if instance.charttime is not None and instance.charttime.tzinfo is None:
        instance.charttime = instance.charttime.replace(tzinfo=get_current_timezone())
    if instance.storetime is not None and instance.storetime.tzinfo is None:
        instance.storetime = instance.storetime.replace(tzinfo=get_current_timezone())


@receiver(pre_save, sender=ChartEvent)
def chartevent_pre_save_handler(sender, instance, **kwargs):
    # add default timezone to unaware date/time fields
    if instance.charttime is not None and instance.charttime.tzinfo is None:
        instance.charttime = instance.charttime.replace(tzinfo=get_current_timezone())
    if instance.storetime is not None and instance.storetime.tzinfo is None:
        instance.storetime = instance.storetime.replace(tzinfo=get_current_timezone())
