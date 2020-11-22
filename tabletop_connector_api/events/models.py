import uuid

from django.db import models


# Create your models here.
from tabletop_connector_api.users.models import User


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=128)
    postal_code = models.CharField(max_length=6)
    number = models.CharField(max_length=64)


class Chat(models.Model):
    pass


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    date = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)
    chat = models.ForeignKey(Chat, null=True, on_delete=models.SET_NULL)
