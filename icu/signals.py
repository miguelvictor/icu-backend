from datetime import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver
from id_validator import validator

from .models import Patient
from .validators import validate_national_id


@receiver(pre_save, sender=Patient)
def pre_save_handler(sender, instance, **kwargs):
    # validate and get info from the patient's national ID
    validate_national_id(instance.national_id)
    info = validator.get_info(instance.national_id)

    # patient's gender and date of birth can be retrieved from info
    instance.gender = "M" if info["sex"] == 1 else "F"
    instance.date_of_birth = datetime.strptime(info["birthday_code"], r"%Y-%m-%d")

    # a default address can also be added if the instance doesn't have one
    if not instance.address:
        instance.address = info["address"]
