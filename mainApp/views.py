from django.shortcuts import render, redirect
import smtplib
from django.contrib import messages
import boto3

AWS_REGION = "ap-south-1"
ssm_client = boto3.client("ssm", region_name=AWS_REGION)
# get_response = ssm_client.get_parameter(Name='SECRET', WithDecryption=True)

def mail(name, email, message):
    EMAIL = ssm_client.get_parameter(Name='contact_email', WithDecryption=True)['Parameter']['Value']
    PASSWORD = ssm_client.get_parameter(Name='contact_password', WithDecryption=True)['Parameter']['Value']

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
