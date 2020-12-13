from unittest import TestCase

import pytest

from tabletop_connector_api.events.serializers import AddressCreateSerializer, AddressSerializer
from tabletop_connector_api.events.test.factories import AddressFactory


@pytest.mark.django_db
class AddressCreateSerializerTest(TestCase):

    def setUp(self):
        self.address_create_serializer = AddressCreateSerializer()
        self.valid_address = {'country': 'Poland', 'city': 'Gdansk',
                              'street': 'Wita Stwosza', 'postal_code': 'aa', 'number': '22'}

        self.invalid_address = {'country': '', 'city': '',
                                'street': 'a' * 40, 'postal_code': '', 'number': ''}

    def test_serializer_with_valid_address(self):
        assert self.address_create_serializer.create(validated_data=self.valid_address) is not None

    def test_serializer_with_invalid_address(self):
        assert self.address_create_serializer.create(validated_data=self.invalid_address) is None


@pytest.mark.django_db
class AddressSerializerTest(TestCase):
    def setUp(self):
        self.address_serializer = AddressSerializer()
        self.valid_address = {'country': 'Poland', 'city': 'Gdansk',
                              'street': 'Wita Stwosza', 'postal_code': 'aa', 'number': '22'}

        self.invalid_address = {'country': '', 'city': '',
                                'street': 'a' * 40, 'postal_code': '', 'number': ''}

    def test_update_valid_data(self):
        address = AddressFactory()
        assert self.address_serializer.update(instance=address, validated_data=self.valid_address) is not None

    def test_update_invalid_data(self):
        address = AddressFactory()
        assert self.address_serializer.update(instance=address, validated_data=self.invalid_address) is None
