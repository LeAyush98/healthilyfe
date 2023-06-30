from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dataApp.forms import HealthDataForm, CalculationsForm
from dataApp.models import HealthData, Calculation
import datetime
import math
import pandas as pd
import seaborn as sb
import matplotlib.pylab as plt
import asyncio

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

def make_weight_dict(request):
    health_data = HealthData.objects.filter(user_id = request.user.id , health_data = "height weight")
    weight_dict = {}
    for index, _ in enumerate(health_data):
        weight_dict[index] = {"id" : index+1, "name" : _.user.first_name, "age" : _.age, "weight" : int(_.data_value.split("/")[1]), "time" : _.date_time.split(" - ")[0]}
    return weight_dict

def make_bmi_dict(request):
    calculated_data = Calculation.objects.filter(user_id = request.user.id, health_data = "bmi")
    bmi_dict = {}
    for index, _ in enumerate(calculated_data):
        bmi_dict[index] = {"id" : index+1, "name" : _.user.first_name, "bmi" : float(_.data_value)}
    return bmi_dict    

def plot_weight(weight_df):
    sb.set_theme(style="ticks", font_scale=1.25)
    g = sb.relplot(
        data=weight_df,
        x="id", y="weight", hue= "age",
        palette="crest", marker="^", s=100,
    )
    g.set_axis_labels("Count", "Weight (Kg)", labelpad=10)
    g.figure.set_size_inches(6.5, 4.5)
    g.ax.margins(.15)
    g.despine(trim=True)
    plt.savefig("static/images/weight.png")
    plt.close()

def plot_bmi(bmi_df):
    sb.set_theme(style="ticks", font_scale=1.25)
    h = sb.relplot(
        data=bmi_df,
        x="id", y="bmi", hue= "name",
        palette="crest", marker="v", s=100,
    )
    h.set_axis_labels("Count", "Body Mass Index", labelpad=10)
    h.figure.set_size_inches(6.5, 4.5)
    h.ax.margins(.15)
    h.despine(trim=True)
    plt.savefig("static/images/bmi.png")
    plt.close()

async def save_plots(weight_df, bmi_df):
    plot_weight(weight_df)
    await asyncio.sleep(0.1)  # Add a small delay to allow the GUI to update
    plot_bmi(bmi_df)

# Create your views here.
@login_required
def initial(request):
    user = User.objects.get(id = request.user.id)
    form = HealthDataForm()
    if request.method == "POST":
        form = HealthDataForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["health_data"] == "height weight":
                if "/" in form.cleaned_data["data_value"]: 
                    pass
                else:
                    messages.error(request, "Please add the data with mentioned format...")
                    return redirect('initial')
            
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
    health_data = HealthData.objects.filter(user_id = request.user.id , health_data = "height weight")
    weight_dict = make_weight_dict(request)
    weight_df = pd.DataFrame.from_dict(weight_dict, orient='index')


    calculated_data = Calculation.objects.filter(user_id = request.user.id, health_data = "bmi")
    bmi_dict = make_bmi_dict(request)
    bmi_df = pd.DataFrame.from_dict(bmi_dict, orient='index')
    try:
        asyncio.run(save_plots(weight_df , bmi_df))
    except ValueError:
        pass   

    return render(request, "dataApp/final.html", {"health_data" : health_data, "calculated_data" : calculated_data})

@login_required
def delete_health_data(request, id):
    data = HealthData.objects.get(id = id)
    if data.user_id == request.user.id:
        data.delete()
        messages.success(request, "Data deleted successfully.")
        return redirect("final")
    else:
        messages.error(request, "You do not have permission to do that.")
        return redirect('home')

@login_required
def delete_calc_data(request, id):
    data = Calculation.objects.get(id = id)
    if data.user_id == request.user.id:
        data.delete()
        messages.success(request, "Data deleted successfully.")
        return redirect("final")
    else:
        messages.error(request, "You do not have permission to do that.")
        return redirect('home')
