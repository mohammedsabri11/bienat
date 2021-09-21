from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    name=models.CharField(max_length=30)
    birthday = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return '{}  {} '.format(self.name,

                                self.username,

                                )
