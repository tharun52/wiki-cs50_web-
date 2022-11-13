from django.shortcuts import render
#from django.urls import is_valid_path
import markdown
from . import util
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from random import randint

#form class
class SearchForm(forms.Form):
    item = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'search', 'placeholder': 'Search'}))

class NewForm(forms.Form):
    title = forms.CharField(label="Title : ", max_length=50, widget=forms.TextInput(attrs={'class' : 'search1' , 'placeholder':'Title'}))    
    content = forms.CharField(label="Content : ", widget=forms.Textarea(attrs={'class' : 'area', 'placeholder': 'Markdowned content', "rows":"5"}))

class EditForm(forms.Form):
    edit = forms.CharField(label = "", widget=forms.Textarea(attrs={'class':'area'}))

def index(request):
    entries = util.list_entries()
    searched=[]
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["item"]
            for i in entries:
                if title in entries:
                    content=markdown.markdown(util.get_entry(title))
                    context = {
                        "title": title.capitalize(),
                        "content": content,
                        'form' : SearchForm()
                    }
                    return render(request, "encyclopedia/entry.html", context)
                if title.lower() in i.lower():
                    searched.append(i)
                    context = {
                        "searched" : searched,
                        "form" : SearchForm()
                    }
            return render(request, "encyclopedia/search.html", context)
        else:
            return render(request, "encyclopedia/index.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form" : SearchForm()
        })

def edit(request, title):          
    if request.method == "GET":
        page = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title.capitalize(),
            "edit" : EditForm(initial={"edit" : page}),
            "form" : SearchForm()
        })
    else:
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["edit"]
            util.save_entry(title.capitalize(), content)
            return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))

def entry(request, title):
    entries = util.list_entries()
    if title.upper() in map(str.upper, entries):
        content=markdown.markdown(util.get_entry(title))
        return render(request, "encyclopedia/entry.html", {
            "title": title.capitalize(),
            "content": content,
            "form" : SearchForm()
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title.capitalize(),
            "content": "Sorry, entry not found",
            "form" : SearchForm()
        })

def new(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            entries = util.list_entries()
            if title.upper() in map(str.upper, entries):
                return render(request, "encyclopedia/error.html", {
                    "form": SearchForm(),
                    "Message": "Page Already exists"
                })
            else:
                util.save_entry(title.capitalize(), content)
                content = markdown.markdown(content)
                return render(request, "encyclopedia/entry.html", {
                    "title": title.capitalize(),
                    "content": content,
                    "form" : SearchForm()
                })
    else:
        return render(request, "encyclopedia/new.html", {
            "form" : SearchForm(),
            "new_form" : NewForm()
        })

def random(request):
    entries = util.list_entries()
    title = entries[randint(0, len(entries)-1)]
    return HttpResponseRedirect(reverse("entry", kwargs={"title":title}))