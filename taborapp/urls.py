from django.conf.urls import include, url
from taborapp.views import index, gallery, adminLogin, adminPanel

# TODO: admin needs only one view, we keep two just because it was easier to create

urlpatterns = [
    url(r'^$', index),
    url(r'^gallery/', gallery),
    url(r'^adminPanel/', adminPanel)
    url(r'^adminLogin/', adminLogin),
]

