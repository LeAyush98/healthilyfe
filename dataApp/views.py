from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dataApp.forms import HealthDataForm, CalculationsForm
from dataApp.models import HealthData, Calculation
import datetime
import inspect
import math

def date_time():
    date = datetime.datetime.now()
    date = date.strftime("%B %d, %Y - %H:%M")
    return date

def root(request) -> HealthData:
    check = False
    health_data = HealthData.objects.filter(user_id = request.user.id)
    for data in reversed(health_data):
        if data.health_data == "height weight":
            check = True
            return data
    if not check:
        messages.error(request, f"Please add height and weight data first, {request.user.first_name}")
         

def bmi(request, health_data: HealthData, from_body_fat:bool = False):
    height = float(health_data.data_value.split("/")[0])
    weight = float(health_data.data_value.split("/")[1])
    bmi = (weight) / (height * height)
    if not from_body_fat:
        messages.success(request, f"Hello {request.user.first_name}, Your BMI is {round(bmi,1)}")
    Calculation.objects.create(health_data = "bmi", data_value = round(bmi,1), user_id = request.user.id, date_time = date_time())    
    return round(bmi,1)

def ideal_weight(request, health_data: HealthData):
    gender = health_data.gender
    height = float(health_data.data_value.split("/")[0])
    if gender == "male":
        iw = 56.2 + (1.41 * ((height - 1.524) / 0.0254))
    if gender == "female":
        iw = 53.1 + (1.36 * ((height - 1.524) / 0.0254))
    Calculation.objects.create(health_data = "ideal weight", data_value = math.floor(iw), user_id = request.user.id, date_time = date_time())        
    messages.success(request, f"Hello {request.user.first_name}, Your ideal weight is {math.floor(iw)} kg")

def calorie(request, health_data: HealthData):
    gender = health_data.gender
    height = float(health_data.data_value.split("/")[0])
    weight = float(health_data.data_value.split("/")[1])
    age = int(health_data.age)
    if gender == "male":
        cal = (10 * weight) + (625 * height) - (5 * age) + 5
    if gender == "female":
        cal = (10 * weight) + (625 * height) - (5 * age) - 161
    Calculation.objects.create(health_data = "calorie", data_value = math.floor(cal), user_id = request.user.id, date_time = date_time())         
    messages.success(request, f"Hello {request.user.first_name}, You must consume {math.floor(cal)} calories per day")

def body_fat(request, health_data: HealthData):
    gender = health_data.gender
    get_bmi = bmi(request, health_data, True)
    age = int(health_data.age)
    if gender == "male":
        bf = (1.20 * get_bmi) + (0.23 * age) - 16.2
    if gender == "female":
        bf = (1.20 * get_bmi) + (0.23 * age) - 5.4
    Calculation.objects.create(health_data = "body fat", data_value = round(bf,2), user_id = request.user.id, date_time = date_time())        
    messages.success(request, f"Hello {request.user.first_name}, Your Body Fat percentage is {round(bf,2)} %")

# Create your views here.
@login_required
def initial(request):
    user = User.objects.get(id = request.user.id)
    form = HealthDataForm()
    if request.method == "POST":
        form = HealthDataForm(request.POST)
        if form.is_valid():
            HealthData.objects.create(age = form.cleaned_data["age"], health_data = form.cleaned_data["health_data"], data_value = form.cleaned_data["data_value"], 
                       exercise = form.cleaned_data["exercise"], date_time = date_time(), user = user, gender = form.cleaned_data['gender'] )
            messages.success(request, "Would you like to add more?")
            return render(request, "dataApp/initial.html", {"form":form})
        else:
                messages.error(request, "There has been some error...")
                return redirect('initial')

    return render(request, "dataApp/initial.html", {"form":form})

@login_required
def second(request):
    form = CalculationsForm()
    if request.method == "POST":
        form = CalculationsForm(request.POST)
        if form.is_valid():
            data = root(request)    
            if data:
                switch = {
                    'bmi' : bmi,
                    'body fat' : body_fat,
                    'calorie' : calorie,
                    'ideal weight' : ideal_weight
                }

                for key,value in switch.items():
                    if key == form.cleaned_data['health_data']: value(request, data)
    
    return render(request, "dataApp/second.html", {"form" : form})


@login_required
def final(request):
    health_data = HealthData.objects.filter(user_id = request.user.id)
    calculated_data = Calculation.objects.filter(user_id = request.user.id)
    return render(request, "dataApp/final.html", {"health_data" : health_data, "calculated_data" : calculated_data})



