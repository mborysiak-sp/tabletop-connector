from unittest import TestCase

import pytest
from rest_framework import serializers

from tabletop_connector_api.events.serializers import (
    AddressCreateSerializer,
    AddressSerializer,
)
from tabletop_connector_api.events.test.factories import AddressFactory


@pytest.mark.django_db
class AddressCreateSerializerTest(TestCase):
    def setUp(self):
        self.address_create_serializer = AddressCreateSerializer()
        self.valid_address = {
            "country": "Poland",
            "city": "Gdansk",
            "street": "Wita Stwosza",
            "postal_code": "aa",
            "number": "22",
            "geo_x": None,
            "geo_y": None,
        }

        self.invalid_address = {
            "country": "",
            "city": "",
            "street": "a" * 40,
            "postal_code": "",
            "number": "",
            "geo_x": None,
            "geo_y": None,
        }

    def test_serializer_with_valid_address(self):
        assert (
            self.address_create_serializer.create(validated_data=self.valid_address)
            is not None
        )

    def test_serializer_with_invalid_address(self):
        self.assertRaises(
            serializers.ValidationError,
            self.address_create_serializer.create,
            self.invalid_address,
        )


@pytest.mark.django_db
class AddressSerializerTest(TestCase):
    def setUp(self):
        self.address_serializer = AddressSerializer()
        self.valid_address = {
            "country": "Poland",
            "city": "Gdansk",
            "street": "Wita Stwosza",
            "postal_code": "aa",
            "number": "22",
            "geo_x": None,
            "geo_y": None,
        }

        self.invalid_address = {
            "country": "",
            "city": "",
            "street": "a" * 40,
            "postal_code": "",
            "number": "",
            "geo_x": None,
            "geo_y": None,
        }

    def test_update_valid_data(self):
        address = AddressFactory()
        assert (
            self.address_serializer.update(
                instance=address, validated_data=self.valid_address
            )
            is not None
        )
