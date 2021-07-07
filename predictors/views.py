from rest_framework.decorators import api_view
from rest_framework.response import Response

from icu.models import Patient

import numpy as np
import random


@api_view(["GET"])
def get_dashboard_info(_):
    patients = random.randint(100, 1000)
    icu_patients = random.randint(100, 400)
    warnings = random.randint(100, 200)
    doctors = random.randint(50, 100)
    trend_patients = random.randint(-100, 100)
    trend_icu_patients = random.randint(-100, 100)
    trend_warnings = random.randint(-40, 40)
    trend_doctors = random.randint(-20, 20)

    return Response(
        {
            "patients": patients,
            "icu_patients": icu_patients,
            "warnings": warnings,
            "doctors": doctors,
            "trend_patients": trend_patients,
            "trend_icu_patients": trend_icu_patients,
            "trend_warnings": trend_warnings,
            "trend_doctors": trend_doctors,
        }
    )


@api_view(["GET"])
def get_dashboard_graph(_):
    return Response(
        {
            "patients": np.random.gamma(1, 2, 14).tolist(),
            "icu_patients": np.random.gamma(1, 2, 14).tolist(),
            "discharged_patients": np.random.gamma(1, 2, 14).tolist(),
        }
    )


@api_view(["GET"])
def get_dashboard_patients(_):
    return Response(
        [
            {
                "subject_id": patient.subject_id,
                "name": patient.name,
                "ward_id": random.randint(101, 999),
                "duration": random.randint(10, 50),
                "is_high_risk": bool(random.getrandbits(1)),
            }
            for patient in Patient.objects.all()[:10]
        ]
    )
