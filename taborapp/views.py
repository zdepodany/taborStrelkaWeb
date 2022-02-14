from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from os import remove
from time import localtime

from .forms import UploadFileForm
from .models import PhotoModel

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

    return render(request, "gallery.html", {
                "page": page,
                "year": year,
                "photos": photos,
                "pages": range(1, pages + 1),
                "max": len(photos) - 1
                })

class DownloadsView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, "downloads.html")

class YearPickView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, "yearPick.html")

class AdminLoginView(LoginView):
    template_name = "login.html"
    next_page = "admin.html"


class AdminView(PermissionRequiredMixin, FormView):
    form_class = UploadFileForm
    template_name = 'admin.html'
    success_url = '/admin/'
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        form = UploadFileForm()

        return render(request, "admin.html", {"username":username, "form":form})

    # 0: Zeroth entry.
    # 1: Override post method for it to handle multiple files.
    def post(self, request, *args, **kwargs):
        form = UploadFileForm()
        files = request.FILES.getlist('file')

        # Validate user

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

        return render(request, "admin.html", {"username":username, "form":form})

