from django.db import models

# Create your models here.
class PhotoModel(models.Model):
    file = models.ImageField(upload_to="photos/%Y/%m/%d/")

class Photos(models.Model):

    class Meta:
        permissions = [
            ("upload", "Can upload photos"),
            ("delete", "Can delete photos"),
        ]


