from django.conf.urls import include, url
from taborapp.views import index, gallery

urlpatterns = [
    url(r'^index/', index),
    url(r'^gallery/', gallery),
]

