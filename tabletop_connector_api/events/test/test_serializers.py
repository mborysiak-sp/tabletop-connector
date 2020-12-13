from unittest import TestCase

import pytest

from tabletop_connector_api.events.serializers import AddressCreateSerializer


@pytest.mark.django_db
class AddressSerializerTest(TestCase):

    def setUp(self):
        self.address_create_serializer = AddressCreateSerializer()


