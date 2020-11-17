import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username


class Game(models.Model):
    id = models.IntegerField(primary_key=True)
    #users = models.ForeignKey(User, on_delete=)


class Address(models.Model):
    pass


class Chat(models.Model):
    pass


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    date = models.DateTimeField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)
    chat = models.ForeignKey(Chat, null=True, on_delete=models.SET_NULL)


