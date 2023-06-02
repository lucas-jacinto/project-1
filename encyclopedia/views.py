from django.shortcuts import render
from django.http  import  HttpResponseRedirect
from django.urls import reverse
from . import util
import markdown
from django import forms


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    markdowner = markdown.Markdown()
    entryPages = util.get_entry(entry)
    if entryPages is None:
        return render(request, "encyclopedia/noExistEntry.html",{
            "entryTitle":entry
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry":markdowner.convert(entryPages),
            "entryTitle": entry
        })

def search(request):
    value = request.GET.get("q",'')
    if(util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': value }))
    else:
        StringEntries = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                StringEntries.append(entry)

        return render(request, "encyclopedia/index.html", {
        "entries": StringEntries,
        "search": True,
        "value": value
    })


def random(request):
    entries = util.list_entries()
    randomEntries = secrets.choice(entries)
    return HttpResponseRedirect(reverse("entry", kwargs={'entry':randomEntries}))