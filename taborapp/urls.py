from django.conf.urls import url, include
# TODO: Port all to classes
from taborapp.views import  (
                        index, gallery, AdminView, AdminLoginView,
                        LogoutView, PasswdView, YearPickView, DownloadsView,
                        DeleteSinglePhotoView, DeleteAllPhotosView,
                        DocumentsUploadView
                    )

urlpatterns = [
    url(r'^$', index),
    url(r'^gallery/', gallery),
    url(r'^admin/', AdminView.as_view()),
    url(r'^yearPick/', YearPickView.as_view()),
    url(r'^downloads/', DownloadsView.as_view()),
    url(r'^login/', AdminLoginView.as_view()),
    url(r'^logout/', LogoutView.as_view()),
    url(r'^passwordChange/', PasswdView.as_view()),
    url(r'^deleteSinglePhoto/', DeleteSinglePhotoView.as_view()),
    url(r'^deleteAllPhotos/', DeleteAllPhotosView.as_view()),
    url(r'^uploadDocuments/', DocumentsUploadView.as_view()),
]

