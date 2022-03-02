# TODO imports need cleaning, the project got reworked

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView

from PIL import Image

from os import remove
from time import localtime
from pathlib import Path

from .forms import UploadFileForm, LoginForm
from .models import PhotoModel

upload_path = Path("media/")

# TODO:
#
# 1) It is a good practice to handle forms with
#    form classes and database models. Do that.

# Helper functions
# TODO: When there are too many, move them somewhere else

def make_thumbnail(file):
    with Image.open(file) as tn:
        size = (16, 16)
        name = Path("thumbnails/") / file.name
        tn.thumbnail(size)
        tn.save(upload_path / name)
        return name.as_posix()

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

    entries = PhotoModel.objects.all().order_by('-id')
    photos = [entry.thumbnail.url for entry in entries]

    return photos, pages

# Create your views here.

def index(request):
    return render(request, "index.html", {})

def gallery(request):
    args = request.GET


    photos, pages = get_photos(0, 0)

    return render(request, "gallery.html", {
                "page": 0,
                "year": 0,
                "photos": photos,
                "pages": range(1, pages + 1),
                "max": len(photos) - 1
                })

class DeleteSinglePhotoView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, "deleteSinglePhoto.html")

class DownloadsView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, "downloads.html")

class YearPickView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, "yearPick.html")

class AdminLoginView(LoginView):
    template_name = "login.html"
    next_page = "/admin/"
    authentication_form = LoginForm

class AdminView(PermissionRequiredMixin, FormView):
    form_class = UploadFileForm

    template_name = "admin.html"
    login_url = "/login/"

    permission_required = ("taborapp.view_photomodel",
                           "taborapp.add_photomodel",
                           "taborapp.delete_photomodel", 
                        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                     

        context["username"] = self.request.user.email

        return context

    def form_valid(self, form):
        for file in form.files.pop("file"):
            thumbnail = make_thumbnail(file)
            pm = PhotoModel(file=file, thumbnail=thumbnail)
            pm.save()
        return HttpResponseRedirect('/admin/')

