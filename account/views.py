from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

# Create your views here.

from account.forms import LoginForm, RegistrationForm


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=request.POST["username"], password=request.POST["password"]
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("lists:index")
        else:
            return render(request, "account/login.html", {"form": form})
    else:
        return render(request, "account/login.html", {"form": LoginForm()})

    return redirect("account:login")


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        checkIfUserExists= User.objects.filter(username= request.POST["username"]).exists()

        if form.is_valid() and not checkIfUserExists:
            User.objects.create_user(
                username=request.POST["username"],
                email=request.POST["email"],
                password=request.POST["password"],
            )
            return redirect("account:login")
        else:
            return render(request, "account/register.html", {"form": form})
    else:
        return render(request, "account/register.html", {"form": RegistrationForm()})


def logout_view(request):
    logout(request)
    return redirect("lists:index")
