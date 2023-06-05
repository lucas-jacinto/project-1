from django.shortcuts import render
from django.http  import  HttpResponseRedirect
from django.urls import reverse
from . import util
import markdown
import secrets
from django import forms
from django.contrib.auth.decorators import login_required


def converterMarkdownToHtml(entry):
    contents = util.get_entry(entry)
    markdowner = markdown.Markdown()
    if contents == None:
        return None
    else:
        return markdowner.convert(contents)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    contentsHtml = converterMarkdownToHtml(entry)
    if contentsHtml == None:
        return render(request, "encyclopedia/noExistEntry.html",{
            "entryTitle": entry
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": contentsHtml,
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



def newEntry(request):
    if request.method == "GET":
       return render(request, "encyclopedia/newEntry.html")

def edit(request, entry):
    return render(request, "encyclopedia/edit.html")
