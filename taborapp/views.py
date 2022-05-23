# TODO imports need cleaning, the project got reworked

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, FormView

from PIL import Image

from os import remove
from time import localtime
from pathlib import Path

from .forms import LoginForm, UploadFileForm, UploadDocForm, PasswdForm
from .models import PhotoModel, DocModel

from zipfile import ZipFile, ZIP_DEFLATED

import json

upload_path = Path("media/")

formnames_mandatory = [
            "Registrace zájemců o přihlášení",
            "Nástupní list",
            "Upozornění rodičů zdravotníkovi",
            "Určení osoby oprávněné dle zák. o zdravotních službách",
            "Souhlas se zpracováním osobních údajů",
            "Posudek o zdravotní způsobilosti dítěte",
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
        size = (256, 256)
        name = Path("thumbnails/") / file.name
        tn.thumbnail(size)
        tn.save(upload_path / name)
        return name.as_posix()

def delete_all(model_class, **kwargs):
    for model in model_class.objects.filter(**kwargs):
        remove(model.file.path)
        model.delete()

    if model_class is PhotoModel:
        photoArchive_regenerate(0)

def delete_selected(model_class, ids):
    for model in model_class.objects.filter(id__in=ids):
        remove(model.file.path)
        remove(model.thumbnail.path)
        model.delete()

    if model_class is PhotoModel:
        photoArchive_regenerate(0)

def get_photos(year, page):
    entries = PhotoModel.objects.filter(year=year).order_by("-id")
    entries_len = entries.count()
    pagesc = entries_len // 16
    if entries_len % 16:
        pagesc += 1

    # Someone asked for a page that doesn't exist
    # Return all non-existent photos
    if pagesc < page:
        return [], range(1, pagesc + 1)

    begin = (page - 1) * 16
    end = page * 16

    photos = [entry.thumbnail.url for entry in entries[begin:end]]

    if pagesc < 8:
        pages = range(1, pagesc + 1)
    else:
        pages = []
        last_skipped = False
        for i in range(1, pagesc + 1):
            if (i < 3 or i > pagesc - 2
               or (i < page + 2 and i > page - 2)):
                pages.append(i)
                if last_skipped:
                    last_skipped = False
            else:
                if not last_skipped:
                    pages.append(-1)
                    last_skipped = True

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

def photoArchive_regenerate(year):
    if not year:
        for i in range(2021, localtime().tm_year + 1):
            photoArchive_regenerate(i)

    zip_path = upload_path / "photos" / f"tabor_archive_{year}.zip"

    if zip_path.is_file():
        remove(zip_path)

    entries = PhotoModel.objects.filter(year=year).order_by("-id")
    with ZipFile(zip_path.as_posix(), mode="w",
            compression=ZIP_DEFLATED) as zipf:
        for entry in entries:
            zipf.write(entry.file.path)


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
                "pages": pages,
                "max": len(photos) - 1
                })

class DeleteSinglePhotoView(PermissionRequiredMixin, TemplateView):
    permission_required = ("taborapp.change_photomodel",
                           "taborapp.add_photomodel",
                           "taborapp.delete_photomodel", 
                        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["username"] = self.request.user.email

        return context

    def get(self, request, *args, **kwargs):
        entries = PhotoModel.objects.all().order_by("-id")
        photos = []
        for entry in entries:
            photo = {}
            photo["url"] = entry.thumbnail.url
            photo["id"] = entry.id
            photos.append(photo)

        return render(request, "deleteSinglePhoto.html", {"photos": photos})

    def post(self, request, *args, **kwargs):
        ids = request.body.decode()
        ids = json.loads(ids)
        delete_selected(PhotoModel, ids)
        return JsonResponse({"status": "TaborwebOk"})

class DeleteAllPhotosView(PermissionRequiredMixin, TemplateView):
    permission_required = ("taborapp.change_photomodel",
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

class PasswdView(PasswordChangeView):
    template_name = "passwd.html"
    success_url = "/login/"
    form_class = PasswdForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["username"] = self.request.user.email

        return context

class AdminView(PermissionRequiredMixin, FormView):
    form_class = UploadFileForm

    template_name = "admin.html"
    login_url = "/login/"

    permission_required = ("taborapp.change_photomodel",
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

        photoArchive_regenerate(year)
        return HttpResponseRedirect('/admin/')

class DocumentsUploadView(PermissionRequiredMixin, FormView):
    form_class = UploadDocForm

    template_name = "uploadDocuments.html"
    login_url = "/login/"

    permission_required = ("taborapp.change_docmodel",
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

