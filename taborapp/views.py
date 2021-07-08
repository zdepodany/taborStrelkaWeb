from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import UploadFileForm
# TODO:
#
# 1) It is a good practice to handle forms with
#    form classes and database models. Do that.

# Helper functions
# TODO: When there are too many, move them somewhere else
def handle_uploaded_file(f):
    with open('tabor.png', 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            handle_uploaded_file(file)
            return HttpResponseRedirect('/admin/')
    else:
        return HttpResponseRedirect('/')

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
    form = UploadFileForm()

    # Do things that require admin auth
    if request.user.is_authenticated:
        # Validate user
        username = session["username"]
        if username != "podany":
            return HttpResponse("Unauthorized", status=401)

        # Handle logging out
        args = request.GET
        out = args.get("logout", None)
        if out:
            logout(request)
            return render(request, "admin.html", {"username":None})

        # Handle file upload
        upload_file(request)

    # Provide login form and handle login
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
                return HttpResponseRedirect('/admin/?login=-1')

    return render(request, "admin.html", {"username":username, "form":form})

