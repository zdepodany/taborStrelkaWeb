from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
    return render(request, "index.html", {})

def gallery(request):
    args = request.GET
    year = args.get("year", 0)

    return render(request, "gallery.html", {"page":1, "year":year})

def admin(request):
    username = None
    session = request.session

    if request.user.is_authenticated:
        args = request.GET
        out = args.get("logout", None)
        if out:
            logout(request)
        else:
            username = session["username"]

    else:
        args = request.POST
        username = args.get("username", None)
        password = args.get("password", None)

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                session["username"] = username
            else:
                # TODO: make this return an invalid login info
                pass

    return render(request, "admin.html", {"user":username})

