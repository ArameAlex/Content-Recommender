from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile = models.ImageField(upload_to='profiles', null=True, blank=True)
    forgot_pass_active_code = models.CharField(max_length=10, null=True, blank=True)
    phone_login_active_code = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=11, unique=True)
    bio = models.CharField(max_length=150, null=True, blank=True)
    def __str__(self):
        return self.username
