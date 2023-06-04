from django.shortcuts import render, redirect
import smtplib
from dotenv import load_dotenv
import os
from django.contrib import messages

load_dotenv(".env")

def mail(name, email, message):
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")

    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=EMAIL, password=PASSWORD)
    connection.sendmail(
        from_addr=email,
        to_addrs=EMAIL,
        msg=f"Subject:Hello!\n\n{message}\n\nThanks and regards,\n{name}"
    )
    connection.close()

# Create your views here.
def home(request):
    if request.method == "POST":
        if request.POST["contactName"] and request.POST["contactEmail"] and request.POST["contactMessage"]:
            name = request.POST["contactName"]
            email = request.POST["contactEmail"]
            message = request.POST["contactMessage"]
            mail(name,email,message)
        else:
            messages.error(request, "Please add all your details before sending message.")    
        return redirect("home")
 
    return render(request, "mainApp/index.html", {})

def about(request):
    return render(request, "mainApp/about.html", {})
