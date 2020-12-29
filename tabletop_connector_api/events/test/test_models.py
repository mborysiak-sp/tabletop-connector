import pytest
from django.db import IntegrityError, DataError
from factory import SubFactory

from tabletop_connector_api.events.models import Address
from tabletop_connector_api.events.test.factories import AddressFactory, EventFactory


@pytest.mark.django_db
class TestAddressModel:
    def test_address_invalid_postal_code(self):
        with pytest.raises(DataError):
            AddressFactory.create(postal_code="*" * 7)

    def test_address_invalid_country(self):
        with pytest.raises(DataError):
            AddressFactory.create(country="*" * 65)

    def test_address_invalid_city(self):
        with pytest.raises(DataError):
            AddressFactory.create(city="*" * 65)

    def test_address_invalid_number(self):
        with pytest.raises(DataError):
            AddressFactory.create(number="*" * 65)

    def test_address_valid(self):
        address = AddressFactory()
        assert Address.objects.count() == 1


@pytest.mark.django_db
class TestEventModel:
    def test_event_invalid_name(self):
        with pytest.raises(DataError):
            EventFactory.create(name="*" * 65)

    def test_event_valid(self):
        event = EventFactory()
        assert Address.objects.count() == 1
