from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    created_at = models.DateField(auto_now_add=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]