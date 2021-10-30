from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

from .managers import CustomUserManager


class User(AbstractUser):

    email = models.EmailField(unique=True)
    is_instructor = models.BooleanField(default=False)
    row_created = models.DateTimeField(default=datetime.now)
    row_last_updated = models.DateTimeField(default=datetime.now)

    objects = CustomUserManager()
