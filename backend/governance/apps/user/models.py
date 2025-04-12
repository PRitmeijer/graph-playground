from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    prefix_last_name = models.CharField(max_length=20, default='')
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name']
    def __str__(self):
        return self.username
    
    @property
    def role(self):
        if self.is_superuser:
            return 'superuser'
        elif self.is_staff:
            return 'admin'
        else:
            return 'user'