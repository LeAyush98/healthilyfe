from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dataApp.forms import HealthDataForm, CalculationsForm
from dataApp.models import HealthData, Calculation
import datetime
import math

def date_time():
    date = datetime.datetime.now()
    date = date.strftime("%B %d, %Y - %H:%M")
    return date

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
            health_data = HealthData.objects.filter(user_id = request.user.id)
            for data in reversed(health_data):
                print(data.user_id)  
                
            return render(request, "dataApp/second.html", {"form" : form})    
    
    return render(request, "dataApp/second.html", {"form" : form})


@login_required
def final(request):
    health_data = HealthData.objects.filter(user_id = request.user.id)
    return render(request, "dataApp/final.html", {"health_data" : health_data})