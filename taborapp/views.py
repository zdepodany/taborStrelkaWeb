from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def hello(request):
   return render(request, "hello.html", {})

def index(request):
   return render(request, "index.html", {})

def gallery(request):
   return render(request, "gallery.html", {})

def gallery2021(request):
   return render(request, "gallery2021.html", {})

def docs(request):
   return render(request, "docs.html", {})

