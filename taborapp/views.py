# TODO imports need cleaning, the project got reworked

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, View

from PIL import Image

from os import remove
from time import localtime
from pathlib import Path

from .forms import LoginForm, UploadFileForm, UploadDocForm
from .models import PhotoModel, DocModel

upload_path = Path("media/")

formnames_mandatory = [
            "Nástupní list",
            "Upozornění rodičů zdravotníkovi",
            "Určení osoby oprávněné",
            "Zpracování osobních údajů",
        ]

formnames_voluntary = [
            "Pokyny pro účastníky tábora",
            "Táborový řád",
        ]

# TODO:
#
# 1) It is a good practice to handle forms with
#    form classes and database models. Do that.
# 2) There are too many helper functions, move them somewhere else
# 3) Get rid of spaghetti code


def make_thumbnail(file):
    with Image.open(file) as tn:
        breakpoint()
        size = (256, 256)
        name = Path("thumbnails/") / file.name
        tn.thumbnail(size)
        tn.save(upload_path / name)
        return name.as_posix()

def delete_all(model_class, **kwargs):
    for model in model_class.objects.filter(**kwargs):
        remove(model.file.path)
        model.delete()

def get_photos(year, page):
    entries = PhotoModel.objects.filter(year=year).order_by("-id")
    pages = entries.count() // 16 + 1

    # Someone asked for a page that doesn't exist
    # Return all non-existent photos
    if pages < page:
        return None, pages

    begin = (page - 1) * 16
    end = page * 16

    photos = [entry.thumbnail.url for entry in entries[begin:end]]

    return photos, pages

def get_docs(amount_mand, amount_vol):
    mandatory = []
    voluntary = []

    for i in range(amount_mand):
        query = DocModel.objects.filter(filetype=i)
        if not query:
            query = None
        else:
            query = query.get()

        mandatory.append(query)


    for i in range(amount_vol):
        query = DocModel.objects.filter(filetype=i+1024)
        if not query:
            query = None
        else:
            query = query.get()

        voluntary.append(query)

    return mandatory, voluntary

# Create your views here.

def index(request):
    return render(request, "index.html", {})

def gallery(request):
    args = request.GET
    year = args.get("year", None)
    page = args.get("page", 1)

    if not year:
        year = request.session.get("year", localtime().tm_year)
    else:
        request.session["year"] = year

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

class DeleteSinglePhotoView(PermissionRequiredMixin, TemplateView):
    permission_required = ("taborapp.view_photomodel",
                           "taborapp.add_photomodel",
                           "taborapp.delete_photomodel", 
                        )

    def get(self, request, *args, **kwargs):
        return render(request, "deleteSinglePhoto.html")

class DeleteAllPhotosView(PermissionRequiredMixin, TemplateView):
    permission_required = ("taborapp.view_photomodel",
                           "taborapp.add_photomodel",
                           "taborapp.delete_photomodel", 
                        )

    def get(self, request, *args, **kwargs):
        delete_all(PhotoModel)
        return HttpResponseRedirect('/admin/')

class DownloadsView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        manlen = len(formnames_mandatory)
        vollen = len(formnames_voluntary)

        mandatory_docs, voluntary_docs = get_docs(manlen, vollen)

        mandatory = []
        voluntary = []

        for i in range(manlen):
            if mandatory_docs[i]:
                doc = mandatory_docs[i].file.name.rsplit("/")[-1]
                url = mandatory_docs[i].file.url
            else:
                doc = "Not Found"
                url = ""

            segment = {
                    "url": url,
                    "doc": doc,
                    "name": formnames_mandatory[i],
                }
            mandatory.append(segment)

        for i in range(vollen):
            if voluntary_docs[i]:
                doc = voluntary_docs[i].file.name.rsplit("/")[-1]
                url = voluntary_docs[i].file.url
            else:
                doc = "Not Found"
                url = ""

            segment = {
                    "url": url,
                    "doc": doc,
                    "name": formnames_voluntary[i],
                }
            voluntary.append(segment)

        context["username"] = self.request.user.email
        context["mandatory"] = mandatory
        context["voluntary"] = voluntary

        return context
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data()
        return render(request, "downloads.html", ctx)

class YearPickView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, "yearPick.html")

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')

class AdminLoginView(LoginView):
    template_name = "login.html"
    next_page = "/admin/"
    authentication_form = LoginForm
    redirect_authenticated_user = True

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
        year = localtime().tm_year
        for file in form.files.pop("file"):
            thumbnail = make_thumbnail(file)
            pm = PhotoModel(file=file, thumbnail=thumbnail, year=year)
            pm.save()
        return HttpResponseRedirect('/admin/')

class DocumentsUploadView(PermissionRequiredMixin, FormView):
    form_class = UploadDocForm

    template_name = "uploadDocuments.html"
    login_url = "/login/"

    permission_required = ("taborapp.view_docmodel",
                           "taborapp.add_docmodel",
                           "taborapp.delete_docmodel", 
                        )


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        manlen = len(formnames_mandatory)
        vollen = len(formnames_voluntary)

        mandatory_docs, voluntary_docs = get_docs(manlen, vollen)

        mandatory = []
        voluntary = []

        for i in range(manlen):
            if mandatory_docs[i]:
                doc = mandatory_docs[i].file.name.rsplit("/")[-1]
            else:
                doc = "Not Found"

            segment = {
                    "doc": doc,
                    "name": formnames_mandatory[i],
                }
            mandatory.append(segment)

        for i in range(vollen):
            if voluntary_docs[i]:
                doc = voluntary_docs[i].file.name.rsplit("/")[-1]
            else:
                doc = "Not Found"

            segment = {
                    "doc": doc,
                    "name": formnames_voluntary[i],
                }
            voluntary.append(segment)

        context["username"] = self.request.user.email
        context["mandatory"] = mandatory
        context["voluntary"] = voluntary

        return context

    def form_valid(self, form):
        filetype = form.cleaned_data["filetype"]
        delete_all(DocModel, filetype=filetype)
        doc = DocModel(**form.cleaned_data)
        doc.save()
        return HttpResponseRedirect('/admin/')

    def form_invalid(self, form):
        return HttpResponseRedirect('/admin/')

