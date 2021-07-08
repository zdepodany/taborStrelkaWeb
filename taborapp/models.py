from django.db import models

# Create your models here.
class PhotoModel(models.Model):
    file = models.FileField(upload_to="taborapp/userdata/photos/%Y/%m/%d/")

