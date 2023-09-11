from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from random import choice
from . import util
from django import forms

class CreateTextareaForm(forms.Form):
    my_title= forms.CharField(
        widget= forms.TextInput(attrs={
            'style':'width: 70vw',
            'placeholder': 'Enter Title'
        }),
        label=""
    )
    my_textarea= forms.CharField(
        widget=forms.Textarea(attrs={
            'style': 'margin-top: 20px; width: 70vw; height: 60vh',
            'placeholder': 'Enter MarkDown Content'
        }),
        label=""
    )

class EditTextareaForm(forms.Form):
    textarea_edit= forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={'style': 'width: 60vw; height: 60vh'}
        ), 
        
    )

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def greed(request, name):
    for entry in util.list_entries():
        if name.lower() == entry.lower():
            html_content= util.convertToHTML(entry)
            return render(request, "encyclopedia/greed.html",{
                "util": html_content,
                "title": name
            })
    return render(request, "encyclopedia/greed.html")

def serch(request):
    serch_result_page= []
    if request.method=="POST":
        serch_text= str(request.POST['q'])
        entries= util.list_entries()
        
        for entry in entries:
            if serch_text.lower()==entry.lower():
                return HttpResponseRedirect(reverse("encyclopedia:greed", args=[entry]))
            elif serch_text.lower() in entry.lower():
                serch_result_page.append(entry)
        return render(request, "encyclopedia/serch_result_page.html",{
            "entries": serch_result_page
        })
    else:
        return render(request, "encyclopedia/serch_result_page.html",{
            "entries": serch_result_page
        })
            
def create(request):
    check=False
    if request.method=="POST":
        form= CreateTextareaForm(request.POST)
        if form.is_valid():
            title_data= form.cleaned_data["my_title"]
            textarea_data= form.cleaned_data["my_textarea"]
            for entry in util.list_entries():
                if title_data.lower() == entry.lower():
                    return render(request, "encyclopedia/create.html",{
                        "form": form,
                        "check": True
                    })
            util.save_entry(title_data, textarea_data)
            return HttpResponseRedirect(reverse("encyclopedia:greed", args=[entry]))
        else:
            return render(request, "encyclopedia/create.html",{
                "form": form,
                "check": False
            })
    else:
        return render(request, "encyclopedia/create.html",{
                "form": CreateTextareaForm(),
                "check": False
            })

def edit(request, entry):
    if request.method=="POST":
        form= EditTextareaForm(request.POST)
        if form.is_valid():
            edit_content= form.cleaned_data["textarea_edit"]
            util.save_entry(entry,edit_content)
            return HttpResponseRedirect(reverse("encyclopedia:greed", args=[entry,]))
        else:
            return render(request, "encyclopedia/edit.html",{
                "form": form,
                "entry": entry
            })
    else:
        return render(request, "encyclopedia/edit.html",{
            "form": EditTextareaForm(
                initial={'textarea_edit': util.get_entry(entry)}
            ),
            "entry": entry
        })
     
def random_page(request):
    entries= util.list_entries()
    random_entry= choice(entries)
    return HttpResponseRedirect(reverse("encyclopedia:greed", args=[random_entry]))
        

