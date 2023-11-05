from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import Listing, Bid, Category, Comment
# Create your views here.
def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all().filter(is_active= True)
    })

def create(request):
    if request.method=="POST":
        type= request.POST["category"]
        category= Category.objects.get(name=type)
        try:
            Listing.objects.create(
                title= request.POST["title"],
                decription= request.POST["decription"], 
                create_user= request.user,
                category= category,
                currentbid= float(request.POST["startingbid"]),
                imgurls= request.POST["img_url"]
            )
        except Exception:
            return render(request, "auctions/create.html",{
                'message': "Please Check Against Listing Information"
            })
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        if request.user.is_authenticated:
            return render(request, "auctions/create.html")
        else:
            return HttpResponseRedirect(reverse("users:index"))
        
def listing(request, listing_id):
    _listing= Listing.objects.get(pk=listing_id)

    #To Check if this listing is a previous listing or not
    if request.session.get("listing", listing_id)!=listing_id:
        del request.session["display_num"]
        request.session["listing"]= listing_id
    if "listing" not in request.session:
        request.session["listing"]= listing_id

    #session of bid
    if "bid_massage" not in request.session:
        request.session["bid_massage"]=''
        bid_massage= ''
    else:
        bid_massage= request.session["bid_massage"]
        del request.session["bid_massage"]
    #create session of comment
    if "display_num" not in request.session:
        request.session["display_num"]= 4
    if not request.session.get(f"comment_{listing_id}"):
        #Get all comment id of 1 listing to session
        request.session[f"comment_{listing_id}"]= [cmt.id for cmt in _listing.comment.all()]
        
    
    #Get list id and list objects of comment need display
    lst_cmt_id= request.session[f"comment_{listing_id}"][None:request.session["display_num"]]
    display_cmt= [Comment.objects.get(pk=id) for id in lst_cmt_id]
    del lst_cmt_id

    
    #Bid announces
    list_bid= _listing.bidlist.all()
    _case= 2
    try:
        if list_bid.get(bid=_listing.currentbid).bidder==request.user:
            _case=1
    except ObjectDoesNotExist:
        pass
    if not request.user.is_authenticated or not list_bid.filter(bidder= request.user).exists():
        _case=0

    #check watchlist   
    in_watchlist= _listing.watchlist.all().filter(id= request.user.id).exists()

    if _listing.is_active:
        return render(request, "auctions/listing.html", {
            'listing': _listing,
            'num_of_bid':  _listing.bidlist.count(),
            'case': _case,
            'in_watchlist': in_watchlist,
            'bid_massage': bid_massage,
            'comments': display_cmt
        })
    else:
        return render(request, "auctions/close.html", {
            'listing': _listing,
            'in_watchlist': in_watchlist,
            'bid_massage': bid_massage,
            'comments': display_cmt,
            'winner': _listing.winner
        })

def categories(request):
    if request.method=="POST":
        _type= request.POST["type"]
        list_item= Category.objects.get(name=_type).listcategory.all().filter(is_active= True)

        if not list_item:
            return render(request, "auctions/category.html", {
            "announce": "Not Have Listing In This Category"
        })
        return render(request, "auctions/category.html", {
            "categorylist": list_item
        })
        
    else:
        category= Category.objects.all()
        return render(request, "auctions/categories.html", {
            'categories': category
        })
    
def watchlist(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:index"))
    if "list_listing" not in request.session:
        request.session["list_listing"]= [listing.id for listing in request.user.watchlist.all()]
    if request.session["list_listing"]!= len(request.user.watchlist.all()):
        request.session["list_listing"]= [listing.id for listing in request.user.watchlist.all()]
    if request.method=="POST":
        listing_id= int(request.POST["listing_id"])
        if not listing_id in request.session["list_listing"]:
            Listing.objects.get(pk=listing_id).watchlist.add(request.user)
            request.session["list_listing"].append(listing_id)
            request.session.modified= True
        else:
            Listing.objects.get(pk=listing_id).watchlist.remove(request.user)
            request.session["list_listing"].remove(listing_id)
            request.session.modified = True
        return HttpResponseRedirect(reverse("auctions:listing", args=[listing_id,]))
    else:
        listings= [Listing.objects.get(id=index) for index in request.session["list_listing"]]
        return render(request, "auctions/watchlist.html", {
            "listings": listings
        })

def place_bid(request, listing_id):
    if request.method=="POST" and request.user.is_authenticated:
        bid= float(request.POST["bid"])
        _listing = Listing.objects.get(pk=listing_id)
        if bid > _listing.currentbid:
            _listing= Listing.objects.get(pk=listing_id)
            _listing.currentbid= bid
            _listing.save()

            _bid= Bid.objects.create(
                bidder= request.user,
                bid= bid,
                listing= Listing.objects.get(pk=listing_id)
            )
            _bid.save()

            # exists session sovling
            if "bid_massage" in request.session:
                del request.session["bid_massage"]
            return HttpResponseRedirect(reverse("auctions:listing", args=[listing_id,]))
        else:
            request.session["bid_massage"]= 'The bid must have more than current bid'
            return HttpResponseRedirect(reverse("auctions:listing", args=[listing_id,]))
    else:
        return HttpResponseRedirect(reverse("users:index"))

def comment(request, listing_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:index"))
    if request.method=="POST":
        _listing= Listing.objects.get(pk=listing_id)
        if request.POST.get("submit","")=="Comment":
            cmt= Comment.objects.create(
                author= request.user,
                content= request.POST["content"],
                listing= _listing
            )
            cmt.save()
            request.session["display_num"]+=1
            #Insert in to beginning of session
            request.session[f"comment_{listing_id}"]= [cmt.id,] + request.session[f"comment_{listing_id}"]
            return HttpResponseRedirect(reverse("auctions:listing", args=[listing_id,]))
        if request.POST["more_cmt"]=="Display More Comments":
            request.session["display_num"]+=5
            return HttpResponseRedirect(reverse("auctions:listing", args=[listing_id,]))
        
def close(request, listing_id):
    if request.method=="POST":
        _listing= Listing.objects.get(pk=listing_id)
        _listing.is_active= False
        if _listing.bidlist.all().filter(bid= _listing.currentbid).exists():
            _listing.winner= _listing.bidlist.all().get(bid= _listing.currentbid).bidder
        _listing.save()
        return HttpResponseRedirect(reverse("auctions:listing", args=[listing_id,]))

        
        
        

