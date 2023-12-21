from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

from django.contrib.auth.models import BaseUserManager
from django.utils import timezone

# To make it possible for superusers to be created without using username
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)




class UserModel(AbstractUser):
    username = models.CharField(null=False, blank=True, max_length=100)
    first_name = models.CharField(max_length=100)
    other_names = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.first_name

    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = [
        'first_name'
    ]
    objects = CustomUserManager()
    