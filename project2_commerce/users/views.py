from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import User
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, "users/index.html")
    else:
        return HttpResponseRedirect(reverse("auctions:index"))

def login_view(request):
    if request.method== "POST":
        username= request.POST["username"]
        password= request.POST["password"]
        user= authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("users:index"))
        else:
            return render(request, "users/login.html", {
                'message': "Username Or Password Not Correct, Please Try Against!",
                'user': user
            })
    else:
        return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return render(request, "users/index.html", {
        'message': "Logged Out"
    }) 

def register(request):
    if request.method=="POST":
        first_name= request.POST["first"]
        last_name= request.POST["last"]
        email= request.POST["email"]
        username= request.POST["username"]
        password= request.POST["password"]
        confirmation= request.POST["confirmation"]
        if password!=confirmation:
            return render(request, "users/register.html", {
                'message': "Password Must Match confirmation"
            })
        try:
            user= User.objects.create_user(
                username= username,
                password= password,
                email= email,
                first_name= first_name,
                last_name= last_name
            )
            user.save()
        except IntegrityError:
            return render(request, "users/register.html", {
                'message': "Username Already Taken"
            })
        login(request,user)
        return HttpResponseRedirect(reverse("users:index"))
    else:
        return render(request, "users/register.html")

def changing(request):
    if request.method=="POST":
        password= request.POST["password"]
        new_password= request.POST["newpassword"]
        confirmation= request.POST["confirm"]
        user= authenticate(request, username= request.user.username, password= password)
        if user is None:
           return render(request, 'users/changing.html',{
                'message': 'Password not correctly!'
            })
        elif new_password!=confirmation:
            return render(request, 'users/changing.html',{
                'message': 'Confirmation must true!'
            })
        user.set_password(new_password)
        user.save()
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, 'users/changing.html')
