import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    firstname = models.TextField(blank=True, null=True, max_length=64)
    lastname = models.CharField(blank=True, null=True, max_length=64)
    date_joined = models.DateTimeField(auto_now_add=True)
