from datetime import datetime

import pytz
from factory import SubFactory
from factory.django import DjangoModelFactory

from tabletop_connector_api.events.models import Address, Event


class AddressFactory(DjangoModelFactory):
    class Meta:
        model = Address

    country = 'Poland',
    city = 'Gdansk',
    street = 'Podwale Grodzkie',
    number = 2,
    postal_code = '80-895'
    geo_x = 0.0
    geo_y = 0.0


class EventFactory(DjangoModelFactory):
    class Meta:
        model = Event

    name = "test"
    date = datetime(2020, 12, 25, 11, 0, tzinfo=pytz.UTC)
    creator = None
    address = SubFactory(AddressFactory)
    chat = None
