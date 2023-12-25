from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserModel

# Register your models here.
admin.site.register(UserModel, UserAdmin)