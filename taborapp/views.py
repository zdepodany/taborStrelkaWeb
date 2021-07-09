from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, FormView
from .forms import UploadFileForm
from .models import PhotoModel
from time import localtime
from os import remove

# TODO:
#
# 1) It is a good practice to handle forms with
#    form classes and database models. Do that.

# Helper functions
# TODO: When there are too many, move them somewhere else
# 1 post
def upload_file(request, form, files):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        for file in files:
            pm = PhotoModel(file=file)
            pm.save()
        return HttpResponseRedirect('/admin/')
    else:
        return HttpResponseRedirect('/')
# 1 post end

def delete_all():
    for model in PhotoModel.objects.all():
        remove(model.file.path)
        model.delete()

def get_photos(year, page):
    pages = PhotoModel.objects.all().count() // 16 + 1

    # Someone asked for a page that doesn't exist
    # Return all non-existent photos
    if pages < page:
        return None, pages

    begin = (page - 1) * 16
    end = page * 16

    entries = PhotoModel.objects.all().order_by('-id')[begin:end]
    photos = [entry.file.url for entry in entries]
    return photos, pages

# Create your views here.

def index(request):
    return render(request, "index.html", {})

def gallery(request):
    args = request.GET
    year = args.get("year", localtime().tm_year)
    page = args.get("page", 1)

    year = int(year)
    page = int(page)

    photos, pages = get_photos(year, page)

    return render(request, "gallery.html", {"page": page, "year": year, "photos": photos,
                                            "pages": range(1, pages + 1)})

# This class is a terrific example of spaghetti, but it should make it work for now.
# TODO TODO TODO 
# TODO TODO TODO 
# TODO TODO TODO 

# I'm gonna keep a very awful comment-based log of changes so future Marcel has
# any chance of fixing this mess. Also, here is one more TODO
class AdminView(FormView):
    form_class = UploadFileForm
    template_name = 'admin.html'  # Replace with your template.
    success_url = '/admin/'  # Replace with your URL or reverse().

    # 0: Zeroth entry
    def get(self, request, *args, **kwargs):
        username = None
        session = request.session
        form = UploadFileForm()

        # Do things that require admin auth
        if request.user.is_authenticated:
            # Validate user
            username = session["username"]
            if username != "podany":
                return HttpResponse("Unauthorized", status=401)

        # Provide login form and handle login

        return render(request, "admin.html", {"username":username, "form":form})

    # 0: Zeroth entry.
    # 1: Override post method for it to handle multiple files.
    def post(self, request, *args, **kwargs):
        username = None
        session = request.session
        # 1
        form = UploadFileForm()
        files = request.FILES.getlist('file')
        # 1 END

        # Do things that require admin auth
        if request.user.is_authenticated:
            # Validate user
            username = session["username"]
            if username != "podany":
                return HttpResponse("Unauthorized", status=401)

            # Handle logging out
            args = request.POST
            out = args.get("logout", None)
            delet = args.get("delete_all", None)
            if out:
                logout(request)
                return render(request, "admin.html", {"username":None})
            if delet:
                delete_all()
                return render(request, "admin.html", {"username":username})

            # Handle file upload
            # 1
            # - upload_file(request)
            upload_file(request, form, files)
            # 1 END

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

