from django.urls import path
from . import views

app_name= "auctions"
urlpatterns= [
    path('',views.index, name="index"),
    path('create/', views.create, name="create"),
    path('<int:listing_id>/', views.listing, name="listing"),
    path('categories/', views.categories, name="categories"),
    path('watchlist/', views.watchlist, name="watchlist"),
    path('<int:listing_id>/bid', views.place_bid, name="place_bid"),
    path('<int:listing_id>/comments', views.comment, name="comment"),
    path('<int:listing_id>/close', views.close, name="close")
]