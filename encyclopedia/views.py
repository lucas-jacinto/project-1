from django.shortcuts import render
from django.http  import  HttpResponseRedirect
from django.urls import reverse
from . import util
import markdown
import secrets




def converterMarkdownToHtml(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    contentsHtml = converterMarkdownToHtml(title)
    if contentsHtml == None:
        return render(request, "encyclopedia/noExistEntry.html",{
            "entryTitle": title,
            "messageError": "This Page Does not Exist!"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": contentsHtml,
            "entryTitle": entry
        })

def search(request):
    value = request.GET.get("q",'')
    if(util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse("entry", kwargs={'title': value }))
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
    return HttpResponseRedirect(reverse("entry", kwargs={'title':randomEntries}))



def newEntry(request):
    if request.method == "GET":
       return render(request, "encyclopedia/newEntry.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        existingTitle = util.get_entry(title)
        if existingTitle is not None:
            return render(request, "encyclopedia/noExistEntry.html", {
                "messageError": "This Page Already Exist."
            })
        else:
            util.save_entry(title, content)
            contentHtml = converterMarkdownToHtml(title)
            return render(request, "encyclopedia/entry.html",{
                "title": title,
                "content": contentHtml
            })


def edit(request, title):
    return render(request, "encyclopedia/edit.html")
