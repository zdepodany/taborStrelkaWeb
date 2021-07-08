from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, FormView
from .forms import UploadFileForm

UPLOAD_PATH= "taborapp/userdata/photos/"

# TODO:
#
# 1) It is a good practice to handle forms with
#    form classes and database models. Do that.

# Helper functions
# TODO: When there are too many, move them somewhere else
def handle_uploaded_file(f, name):
    with open(name, 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

# 1 post
def upload_file(request, form, files):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            basename = UPLOAD_PATH + "file"
            for order, file in enumerate(files):
                name = basename + f"{order}" + ".jpg"
                handle_uploaded_file(file, name)
            return HttpResponseRedirect('/admin/')
    else:
        return HttpResponseRedirect('/')
# 1 post end

# Create your views here.

def index(request):
    return render(request, "index.html", {})

def gallery(request):
    args = request.GET
    year = args.get("year", 0)

    return render(request, "gallery.html", {"page":1, "year":year})

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
    def get(self, request):
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

            # 1'
            ## Handle file upload
            #upload_file(request)
            # 1' END

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

    # 0: Zeroth entry.
    # 1: Override post method for it to handle multiple files.
    def post(self, request, *args, **kwargs):
        username = None
        session = request.session
        # 1
        #form = UploadFileForm()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file')
        # 1 END

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

