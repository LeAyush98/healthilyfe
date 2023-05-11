from django import forms
from dataApp.models import HealthData, Calculation

class HealthDataForm(forms.ModelForm):
    class Meta:
        model = HealthData
        fields = ("gender", "age", "health_data", "data_value", "exercise")

class CalculationsForm(forms.ModelForm):
    class Meta:
        model = Calculation
        fields = ("health_data",)        