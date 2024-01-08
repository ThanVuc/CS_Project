from django.shortcuts import render, HttpResponseRedirect
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, 'user/index.html')
    else:
        return HttpResponseRedirect(reverse('user:login'))

def loginView(request):
    if request.method=="POST":
        email= request.POST["mail"]
        passwd= request.POST["passwd"]
        user = authenticate(request, username=email, password=passwd)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('mailview:index'))
        else:
            return render(request, 'user/login.html', {
                'message': 'Invalid Email or/and Password'
            })
        
    else:
        return render(request, 'user/login.html')


def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('user:login'))

def register(request):
    if request.method=='POST':
        email= request.POST["mail"]
        passwd= request.POST["passwd"]
        confim= request.POST["confirm"]
        if passwd!=confim:
            return render(request, 'user/register.html',{
                'err': 'Password and Confirmation must match!',
            })
        try:
            user= User.objects.create_user(
                username= email,
                email= email,
                password= passwd
            )
            user.save()
        except IntegrityError as e:
            return render(request, 'user/register.html',{
                'err': "Email address already taken!",
            })
        return render(request, 'user/login.html')
    else:
        return render(request, 'user/register.html')

def changingpasswd(request):
    if request.method=="POST":
        email= request.POST["mail"]
        oldpasswd= request.POST["oldpasswd"]
        newpasswd= request.POST["newpasswd"]
        confirm= request.POST["confirm"]
        if newpasswd!= confirm:
            return render(request, 'user/changingpasswd.html',{
                'message': 'New Password and Confirmation must match!'
            })
        user= authenticate(request, username= email, password= oldpasswd)
        if user is not None:
            user.set_password(newpasswd)
            user.save()
            return render(request, 'user/changingpasswd.html', {
                'message': 'Password was update'
            })
        else:
            return render(request, 'user/changingpasswd.html',{
                'message': 'Email or/and Password is not Found!'
            })
    else:
        return render(request, 'user/changingpasswd.html')

def deleteAcc(request):
    if request.method=="POST":
        email= request.POST["mail"]
        passwd= request.POST["passwd"]
        confirm= request.POST["confirm"]
        if passwd!=confirm:
            return render(request, 'user/deleteacc.html',{
                'message': "Password & confirmation must match!"
            })
        user= authenticate(request, username= email, password= passwd)

        if user is not None:
            user.delete()
            return render(request, 'user/login.html', {
                'message': 'Delete user successful!'
            })

        else:
            return render(request, 'user/deleteacc.html',{
                'message': "Email or/and Password not exist!"
            })
    else:
        return render(request, 'user/deleteacc.html')