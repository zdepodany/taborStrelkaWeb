from django.conf.urls import include, url

urlpatterns = [
    url(r'^hello/', 'taborapp.views.hello'),
    url(r'^index/', 'taborapp.views.index'),
    url(r'^gallery/', 'taborapp.views.gallery'),
    url(r'^gallery2021/', 'taborapp.views.gallery2021'),
]

