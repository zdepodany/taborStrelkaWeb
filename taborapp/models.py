from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class TaborUser(AbstractUser):
    email = models.EmailField('E-mail', unique=True)

class PhotoModel(models.Model):
    file = models.ImageField(upload_to="photos/%Y/%m/%d/")

