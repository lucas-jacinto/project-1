from django.shortcuts import render
from django.http  import  HttpResponseRedirect
from django.urls import reverse
from . import util
from django import forms


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request):
    markdown = Markdown()
    entryPages = util.get_entry(entry)
    if entryPages is None:
        return render(request, "encyclopedia/noExistEntry.html",{
            "entryTitle":entry
        })

def search(request):
    value = request.GET.get("q",'')
    if(util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': value }))
    else:
        StringEntries = []
        for entry in util.list_entries():
            StringEntries.append(entry)