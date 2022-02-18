from django.urls import include, re_path
# TODO: Port all to classes
from taborapp.views import index, gallery, AdminView, LoginView, YearPickView

urlpatterns = [
    re_path(r'^$', index),
    re_path(r'^gallery/', gallery),
    re_path(r'^admin/', AdminView.as_view()),
    re_path(r'^login/', LoginView.as_view()),
    re_path(r'^yearPick/', YearPickView.as_view()),
]

