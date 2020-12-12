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
    geo_x = models.FloatField(null=True, blank=True, default=0.0)
    geo_y = models.FloatField(null=True, blank=True, default=0.0)

    def __str__(self):
        return self.country.__str__() + " " \
               + self.city.__str__() + " " \
               + self.street.__str__() + " " \
               + self.number.__str__() + " " \
               + self.postal_code.__str__() + " " \
               + self.geo_x.__str__() + " " \
               + self.geo_y.__str__()


class Chat(models.Model):
    pass


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    date = models.DateTimeField()
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)
    chat = models.ForeignKey(Chat, null=True, blank=True, on_delete=models.SET_NULL)
    participants = models.ManyToManyField(User, related_name='participants')

    def __str__(self):
        return self.name.__str__() + " "\
               + self.date.__str__() + " "\
               + self.address.__str__()
