from factory.django import DjangoModelFactory

from tabletop_connector_api.events.models import Address, Event


class AddressFactory(DjangoModelFactory):
    class Meta:
        model = Address

    country = 'Poland'
    city = 'Gdansk'
    street = 'Podwale Grodzkie'
    number = 2
    postal_code = '80-895'

class EventFactory(DjangoModelFactory):
    class Meta:
        model = Event

    name = "test"
    date = '2020-12-25'
    creator = None
    address = AddressFactory()
    chat = None
