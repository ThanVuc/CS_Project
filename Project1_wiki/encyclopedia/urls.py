from django.urls import path

from . import views
app_name= 'encyclopedia'
urlpatterns = [
    path("", views.index, name="index"),
    path("serch/",views.serch, name="serch"),
    path("create/", views.create, name="create"),
    path("random/", views.random_page, name="random_page"),
    path("<str:name>/", views.greed, name="greed"),
    path("edit/<str:entry>/", views.edit, name="edit")
]
