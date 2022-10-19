from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    birthdate = models.DateField(auto_now=False, auto_now_add=False)
    bio = models.TextField(null=True, blank=True)
    is_critic = models.BooleanField(null=True, blank=True, default=False)
    updated_at = models.DateTimeField(auto_now=True)
