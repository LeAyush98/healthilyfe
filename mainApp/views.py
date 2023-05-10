from django.shortcuts import render, redirect
import smtplib

def mail(name, email, message):
    EMAIL = "ayu.sharma798@gmail.com"
    PASSWORD = "tsacklmdhsjpvqtx"

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
        name = request.POST["contactName"]
        email = request.POST["contactEmail"]
        message = request.POST["contactMessage"]
        mail(name,email,message)
        return redirect("home")
 
    return render(request, "mainApp/index.html", {})

def about(request):
    return render(request, "mainApp/about.html", {})
