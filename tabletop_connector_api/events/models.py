import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


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
        return (
            self.country.__str__()
            + " "
            + self.city.__str__()
            + " "
            + self.street.__str__()
            + " "
            + self.number.__str__()
            + " "
            + self.postal_code.__str__()
            + " "
            + self.geo_x.__str__()
            + " "
            + self.geo_y.__str__()
        )


class Chat(models.Model):
    pass


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=512)
    image = models.CharField(max_length=512)
    thumbnail = models.CharField(max_length=512)
    min_players = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    max_players = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    playtime = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000)]
    )


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    date = models.DateTimeField()
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)
    chat = models.ForeignKey(Chat, null=True, blank=True, on_delete=models.SET_NULL)
    participants = models.ManyToManyField(User, related_name="participants")
    games = models.ManyToManyField(
        Game, related_name="games", related_query_name="games", blank=True
    )

    def __str__(self):
        return (
            self.name.__str__()
            + " "
            + self.date.__str__()
            + " "
            + self.address.__str__()
        )
