from django.db import models
from users.models import User

# Create your models here.
class Category(models.Model):
    name= models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title= models.CharField(unique=True, max_length=64)
    decription= models.CharField(max_length=512)
    time= models.DateTimeField(auto_now=True)
    watchlist= models.ManyToManyField(User, blank=True, related_name="watchlist")
    create_user= models.ForeignKey(User, on_delete=models.CASCADE, related_name="createlist")
    category= models.ForeignKey(Category, on_delete= models.CASCADE, related_name="listcategory")
    winner= models.ForeignKey(User, null=True ,on_delete=models.CASCADE, related_name="wasbid", blank=True)
    currentbid= models.FloatField()
    imgurls= models.URLField(blank=True)
    is_active= models.BooleanField(default=True)

class Bid(models.Model):
    bidder= models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidders")
    bid= models.FloatField()
    time= models.DateTimeField(auto_now=True)
    listing= models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bidlist")

    def __str__(self):
        return f"{self.bidder.username}: {self.listing.title}"

class Comment(models.Model):
    author= models.ForeignKey(User, on_delete=models.CASCADE, related_name="authors")
    content= models.CharField(max_length=512)
    time= models.DateTimeField(auto_now=True)
    listing= models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment")