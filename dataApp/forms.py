from django import forms
from dataApp.models import HealthData, Calculations

class HealthDataForm(forms.ModelForm):
    class Meta:
        model = HealthData
        fields = ("gender", "age", "health_data", "data_value", "exercise")

class CalculationsForm(forms.ModelForm):
    class Meta:
        model = Calculations
        fields = ("health_data",)        