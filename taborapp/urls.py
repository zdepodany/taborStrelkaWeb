from django.conf.urls import include, url
# TODO: Port all to classes
from taborapp.views import index, gallery, AdminView

urlpatterns = [
    url(r'^$', index),
    url(r'^gallery/', gallery),
    url(r'^admin/', AdminView.as_view()),
]

