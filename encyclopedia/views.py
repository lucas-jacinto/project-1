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


class newEntryForm(forms.Form):
    title = forms.CharField(label = "Entry the Title", widget=forms.TextInput(attrs={'class' : 'form-control col-md-8 col-lg-8'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-md-8 col-lg-8', 'rows': 10}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

def newEntry(request):
    if request.method == "POST":
        form = newEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if(util.get_entry(title) is None or form.cleaned_data["edit"] is True):
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("entry", kwargs={"entry": title}))
            else:
                return render(request, "encyclopedia/newEntry.html", {
                "form" : form,
                "entry" : title,
                "existing" : True
                })
        else:
            return render(request, "encyclopedia/newEntry.html", {
            "form" : form,
            "existing" : False
            })
    else:
        return render(request, "encyclopedia/newEntry.html", {
        "form" : form,
        "existing" :False
        })