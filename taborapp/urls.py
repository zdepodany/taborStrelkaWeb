from django.conf.urls import include, url
from taborapp.views import index, gallery, adminLogin, adminPanel

urlpatterns = [
    url(r'^$', index),
    url(r'^gallery/', gallery),
    url(r'^admin/', admin),
]

