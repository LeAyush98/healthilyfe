from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from authApp.forms import RegisterUserForm, UpdateUserForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Create your views here.
def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = authenticate(request, username=username, password=password, email = email, first_name = first_name, last_name = last_name)
            login(request, user)
            messages.success(request, f"Registration Successful! Welcome {str(username).title()}!")
            return redirect('home')
        else:
            messages.error(request, "There has been some error...")
            return redirect('register')
    else:
        form = RegisterUserForm()
        return render(request, "authApp/register.html", {"form": form})

def update_user(request, id):
    if id == request.user.id:
        user = User.objects.get(id = id)
        form = UpdateUserForm()
        if request.method == "POST":
            form = UpdateUserForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['new_password'] == form.cleaned_data["confirm_password"]:
                    user.username = form.cleaned_data['username']
                    user.password = make_password(form.cleaned_data['new_password'])
                    user.email = form.cleaned_data['email']
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name = form.cleaned_data['last_name']
                    user.save()
                    messages.success(request, "Update Successful!")
                    return redirect("home")
                else:
                    messages.error(request, "The passwords do not match...")
                    return render(request, "authApp/update.html", {"form" : form})
            else:
                messages.error(request, "There has been some error...")
                return redirect('home')

        return render(request, "authApp/update.html", {"form" : form})
    else:
        messages.error(request, "You do not have permission to do that.")
        return redirect('home')

@login_required
def delete_user(request, id):
    if id == request.user.id:
        user = User.objects.get(id = id)
        logout(request)
        user.delete()
        return redirect("home")
    else:
        messages.error(request, "You do not have permission to do that.")
        return redirect('home')

def login_user(request):
    if request.method == "POST":
        username =  request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
           messages.success(request , (f"Log In Successful! Welcome {user.get_username().title()}!"))
           login(request, user)
           return redirect("home")
        
        else:

            messages.warning(request, f"Log In failed, please try again...")
            return redirect("login")

    return render(request, "authApp/login.html", {})

def logout_user(request):
    logout(request) 
    messages.success(request , (f"Log Out Successful! Hope to see you again :))"))   
    return redirect('home')