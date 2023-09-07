from django.shortcuts import render
from django.http import HttpResponse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def greed(request, name):
    for entry in util.list_entries():
        if name == entry.lower():
            return render(request, "encyclopedia/greed.html",{
                "util": util.get_entry(entry)
            })
    return HttpResponse("The Entry Not Exist!")
