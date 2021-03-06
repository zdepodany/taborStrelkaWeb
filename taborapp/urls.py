from django.urls import include, re_path
# TODO: Port all to classes
from taborapp.views import  (
                        index, gallery, AdminView, AdminLoginView,
                        LogoutView, PasswdView, YearPickView, DownloadsView,
                        DeleteSinglePhotoView, DeleteAllPhotosView,
                        DocumentsUploadView
                    )

urlpatterns = [
    re_path(r'^$', index),
    re_path(r'^gallery/', gallery),
    re_path(r'^admin/', AdminView.as_view()),
    re_path(r'^yearPick/', YearPickView.as_view()),
    re_path(r'^downloads/', DownloadsView.as_view()),
    re_path(r'^login/', AdminLoginView.as_view()),
    re_path(r'^logout/', LogoutView.as_view()),
    re_path(r'^passwordChange/', PasswdView.as_view()),
    re_path(r'^deleteSinglePhoto/', DeleteSinglePhotoView.as_view()),
    re_path(r'^deleteAllPhotos/', DeleteAllPhotosView.as_view()),
    re_path(r'^uploadDocuments/', DocumentsUploadView.as_view()),
]

