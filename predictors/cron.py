from icu.models import Patient

from .models import ModelPrediction


def run_model_inference():
    patient = Patient.objects.first()
    prediction = ModelPrediction.objects.create(
        patient=patient,
        inputs={"hey": "yo!"},
        output=0.9999,
    )
    prediction.save()
