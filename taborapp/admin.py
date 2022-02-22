from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TaborUser

admin.site.register(TaborUser, UserAdmin)
