from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class HealthData(models.Model):
    DATA_CHOICES = [("blood pressure","Blood Pressure"), ("height weight", "Height/Weight in m/Kg"), ("heart rate", "Heart Rate in bpm")]
    EXERCISE_CHOICES = [("no", "No Exercise"), ("low", "Low Intensity"), ("mid", "Moderate Workout < 1 hour ") , ("high", "High Intensity Workout")]
    GENDER = [("male","Male"), ("female", "Female")]
    gender = models.CharField(max_length=30, choices=GENDER)
    age = models.IntegerField(choices = [(_,_) for _ in range(10,101)])
    health_data = models.CharField(max_length=30, choices=DATA_CHOICES)
    data_value = models.CharField(max_length=30)
    exercise = models.CharField(max_length=30, choices=EXERCISE_CHOICES)
    date_time = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Calculation(models.Model):
    HEALTH_CHOICES = [("bmi", "BMI Calculator"), ("body fat", "Body Fat Calculator"), ("ideal weight", "Ideal Weight Calculator"), 
                      ("calorie", "Calorie Intake Calculator")]    
    health_data = models.CharField(max_length=30, choices= HEALTH_CHOICES)
    data_value = models.CharField(max_length=30)
    date_time = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)