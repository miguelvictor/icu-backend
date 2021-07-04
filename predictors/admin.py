from django.contrib import admin

from .models import ModelPrediction


class ModelPredictionAdmin(admin.ModelAdmin):
    raw_id_fields = ("patient",)


admin.site.register(ModelPrediction, ModelPredictionAdmin)