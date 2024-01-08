from django.urls import path
from . import views
app_name= 'user'
urlpatterns= [
    path('', views.index, name='index'),
    path('login', views.loginView, name='login'),
    path('logout', views.logoutView, name='logout'),
    path('register', views.register, name='register'),  
    path('changingpasswd', views.changingpasswd, name='changingPasswd'),
    path('deleteacc', views.deleteAcc, name='deleteAcc'),
]