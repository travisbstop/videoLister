from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import AsmrVideo
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import NewUserForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

def home(request):
    videos = AsmrVideo.objects.all()
    return render(request, "main/home.html", {"videos":videos})


def register(request):
    """
    if the request is post, i want to save the form to the User table. Otherwise, I want to 
    display a form that allows the user to input their username, password, and email. 
    """
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            #login the user after registration
            login(request, user)
            #take em home
            return redirect("main:home")
    form = NewUserForm()
    return render(request, "main/register.html", {"form":form})


def loginRequest(request):

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            #returns a user if the username and password match the database. otherwise None.
            user = authenticate(request, username=username, password=password)
            if user != None:
                login(request, user)
                return redirect("main:home")
            
    form = AuthenticationForm()
    return render(request, "main/login.html", {"form":form})

def logoutRequest(request):
    logout(request)
    redirect("main:home")
# Create your views here.
