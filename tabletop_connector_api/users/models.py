import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    firstname = models.TextField(blank=True, null=True, max_length=64)
    lastname = models.CharField(blank=True, null=True, max_length=64)
    date_joined = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(
        upload_to="avatars/", default="avatars/default_avatar.png"
    )
