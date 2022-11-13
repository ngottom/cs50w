import random
from django.shortcuts import render

from . import util

import markdown


def index(request):
    entries = util.list_entries()
    css_file = util.get_entry("CSS")
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)


def entry(request, title):
    htmlContent = convert_md_to_html(title)
    if htmlContent == None:
        return render(request, "encyclopedia/error.html", {
            "message": "this page does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": htmlContent
        })


def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        htmlContent = convert_md_to_html(entry_search)
        if htmlContent:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": htmlContent
            })
        else:
            allEntries = util.list_entries()
            recommendation = []
            for entry in allEntries:
                if entry_search.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommendation": recommendation
            })


def newPage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newPage.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist:
            return render(request, "encyclopedia/error.html", {
                "message": "Entry page already exists"
            })
        else:
            util.save_entry(title, content)
            htmlContent = convert_md_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": htmlContent
            })


def edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })


def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        htmlContent = convert_md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": htmlContent
        })


def randomPage(request):
    allEntries = util.list_entries()
    randomEntry = random.choice(allEntries)
    htmlContent = convert_md_to_html(randomEntry)

    return render(request, "encyclopedia/entry.html", {
        "title": randomEntry,
        "content": htmlContent
    })
