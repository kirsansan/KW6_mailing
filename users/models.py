from django.contrib.auth.models import AbstractUser
from django.db import models

from main.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='email', unique=True)
    phone = models.CharField(max_length=35, verbose_name='phone', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='country', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='avatar', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
