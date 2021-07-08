from django.shortcuts import render
from django.http import HttpResponse
from pprint import pprint

# Create your views here.

def index(request):
    return render(request, "index.html", {"page":0})

def gallery(request):
    args = request.GET
    year = args.get("year", 0)

    return render(request, "gallery.html", {"page":1, "year":year})

def adminPanel(request):
    return render(request, "adminPanel.html", {"page":3})

def adminLogin(request):
    return render(request, "adminLogin.html", {"page":2})
