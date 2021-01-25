from datetime import datetime

import pytz
from factory import SubFactory
from factory.django import DjangoModelFactory

from tabletop_connector_api.chats.models import Chat
from tabletop_connector_api.events.models import Address, Event, Game
from tabletop_connector_api.users.models import User


class AddressFactory(DjangoModelFactory):
    class Meta:
        model = Address

    country = "Poland"
    city = "Gdansk"
    street = "Podwale Grodzkie"
    number = "2"
    postal_code = "80-895"
    geo_x = 0
    geo_y = 0

class GameFactory(DjangoModelFactory):
    class Meta:
        model = Game
    name = "qqeqq"
    image = "aewaea"
    thumbnail = "aeawaeaw"
    min_players = 2
    max_players = 5
    playtime = 50

class ChatFactory(DjangoModelFactory):
    class Meta:
        model = Chat


class EventFactory(DjangoModelFactory):
    class Meta:
        model = Event

    name = "test"
    date = datetime(2025, 12, 25, 11, 0, tzinfo=pytz.UTC)
    creator = None
    address = SubFactory(AddressFactory)
    chat = SubFactory(ChatFactory)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
