from django.shortcuts import redirect, render 
from markdown2 import Markdown
from django import forms
import re
from . import util
import random

class NewPageForm(forms.Form):
    title = forms.CharField(label="", required=True, widget=forms.TextInput(attrs={
        "placeholder":"title"
    }))
    markdown = forms.CharField(label="", required=True, widget=forms.Textarea(attrs={
        "placeholder":"content"
    }))

class EditPageForm(forms.Form):
    title = forms.CharField(label="", required=True, widget=forms.TextInput(attrs={
        "placeholder":"title"
    }))
    markdown = forms.CharField(label="", required=True, widget=forms.Textarea(attrs={
        "placeholder":"content"
    }))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, page):
    markdown = util.get_entry(page)

    if markdown is not None:
        return render(request, "encyclopedia/page.html", {
            "page": page,
            "content": Markdown().convert(markdown)
        })
    else:
        return render(request, "encyclopedia/error.html",{
            "page": page, "message":" could not be found!"
        })

def search(request):
    keyword = request.GET['q' or '']
    if util.is_entry(keyword):
        return redirect('page', page=keyword)
    else:
        results= []
        for entry in util.list_entries():
            if re.findall(keyword, entry, re.IGNORECASE):
                results.append(entry)
        search_results={
            'results': results
        }
        if results == []:
            return render(request, "encyclopedia/error.html",{
            "page": keyword, "message":" could not be found!"
        })
        else:
            return render(
                request,
                'encyclopedia/search.html',
                search_results
            )

def new(request):
    if request.method=="GET":
        return render(request, "encyclopedia/new.html", {
            "form": NewPageForm()
        })
    form = NewPageForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data.get("title")
        markdown = form.cleaned_data.get("markdown")
        if util.is_entry(title):
            return render(request, "encyclopedia/error.html", {"page": title, "message": " does exist already"})
        else:
            util.save_entry(title, markdown)
            return redirect("page", page=title)
        
def edit(request, page):
    if request.method=="GET":
        return render(request, "encyclopedia/edit.html", {
            "form": EditPageForm({'title':page,'markdown':util.get_entry(page)})
        })
    form = EditPageForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data.get("title")
        markdown = form.cleaned_data.get("markdown")
        util.save_entry(title, markdown)
        return redirect("page", page=title)


def randompage(request):
    random.seed(a=None, version=2)
    list_pages = util.list_entries()
    page = list_pages[random.randrange(len(list_pages)-1)]

    markdown = util.get_entry(page)
    return render(request, "encyclopedia/page.html", {
        "page": page,
        "content": Markdown().convert(markdown)
    })