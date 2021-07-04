from django.db import models
from django.utils.translation import ugettext_lazy as _

from icu.models import Patient


class ModelPrediction(models.Model):
    INFERENCE_TYPE_CHOICES = (
        ("sepsis", _("Sepsis")),
        ("mi", _("Myocardial Infarction (MI)")),
        ("vancomycin", _("Vancomycin")),
        ("aki", _("Acute Kidney Injury (AKI)")),
        ("mortality", _("Mortality")),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    inference_type = models.CharField(
        _("Inference Type"),
        max_length=50,
        choices=INFERENCE_TYPE_CHOICES,
    )
    inputs = models.JSONField()
    output = models.FloatField()
    added_at = models.DateTimeField(_("Added At"), auto_now_add=True)

    def __str__(self):
        return f"【{self.patient.name}】的"

    class Meta:
        indexes = [
            models.Index(fields=["added_at"]),
        ]
        verbose_name = _("Model Prediction")
        verbose_name_plural = _("Model Predictions")
