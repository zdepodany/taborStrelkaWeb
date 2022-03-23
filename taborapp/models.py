from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class TaborUser(AbstractUser):
    email = models.EmailField('E-mail', unique=True)

class PhotoModel(models.Model):
    file = models.ImageField(upload_to="photos/")
    thumbnail = models.ImageField(upload_to="thumbnails/", null=True)

class DocModel(models.Model):
    file = models.ImageField(upload_to="docs/")
    filetype = models.BigIntegerField()

