from django.urls import path
from . import views

app_name= "mailview"
urlpatterns= [
    path('', views.index, name='index'),
    path('home/<str:mail_box>', views.locateMailBox, name='locateMailBox'),
    path('mail/<int:mail_id>', views.detail, name='detail'),
    path('paging/', views.paging, name='paging'),
    #API Routes
    path('emails', views.compose, name='compose'),
    path('emails/<int:mail_id>', views.mail_detail, name='emailDetail'),
    path('emails/<str:mail_box>', views.mailbox, name='mailbox')
]