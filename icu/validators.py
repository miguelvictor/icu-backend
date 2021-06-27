from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from id_validator import validator


def validate_national_id(value: str):
    if not validator.is_valid(value):
        raise ValidationError(
            _("%(value)s is not a valid national ID number."),
            params={"value": value},
        )
