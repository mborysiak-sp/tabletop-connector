from datetime import datetime

import pytest
import pytz
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate

from tabletop_connector_api.events.models import Event
from tabletop_connector_api.events.serializers import EventSerializer
from tabletop_connector_api.events.test.factories import EventFactory, AddressFactory, UserFactory
from tabletop_connector_api.events.views import CustomEventViewSet, EventViewSet
from tabletop_connector_api.users.models import User


@pytest.mark.django_db
class TestCustomEventViewSet(TestCase):

    def setUp(self):
        self.view = CustomEventViewSet.as_view()
        self.factory = APIRequestFactory()

    def test_CustomEventViewSet_found_response_code(self):
        EventFactory.create(address=AddressFactory(geo_x=54.34950, geo_y=18.64847))
        request = self.factory \
            .get('api/geteventbydistance/?distance=10&country=Poland&city=Gdansk&street=Teatralna')

        assert self.view(request).status_code == 200

    def test_CustomEventViewSet_found_in_queryset(self):
        EventFactory.create(address=AddressFactory(geo_x=54.34950, geo_y=18.64847))
        request = self.factory \
            .get('api/geteventbydistance/?distance=10&country=Poland&city=Gdansk&street=Teatralna')

        assert len(self.view(request).data) == 1

    def test_CustomEventViewSet_not_found_response_code(self):
        request = self.factory \
            .get('api/geteventbydistance/?distance=10&country=Poland&city=Gdansk&street=Teatralna')

        assert self.view(request).status_code == 204

    def test_CustomEventViewSet_when_address_no_specified(self):
        request = self.factory \
            .get('api/geteventbydistance/?distance=10')

        assert self.view(request).status_code == 204


@pytest.mark.django_db
class TestAddressViewSet(TestCase):

    def setUp(self):

        self.factory = APIRequestFactory()

    def test_get_all_addresses(self):
        AddressFactory()


@pytest.mark.django_db
class TestEventViewSet(TestCase):

    def setUp(self):

        self.factory = APIRequestFactory()
        self.user = UserFactory()
        self.view = EventViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update'})  # , 'get': 'retrieve'})
        self.example = {'name': 'test',
                        'date': '2020-12-14T20:09:00+0000',
                        'creator': None,
                        'address': {
                            'country': 'Poland',
                            'city': 'Gdansk',
                            'street': 'Wita Stwosza',
                            'postal_code': '21-307',
                            'number': '2'
                            },
                        'chat': None,
                        'participants': None
                        }

    def test_get_all_events(self):

        EventFactory()
        EventFactory(name='test2')
        request = self.factory.get('api/events/')
        force_authenticate(request, user=self.user)
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        self.assertEqual(self.view(request).data['results'], serializer.data)

    def test_get_all_events_status_code(self):
        EventFactory()
        EventFactory(name='test2')
        request = self.factory.get('api/events/')
        force_authenticate(request, user=self.user)

        self.assertEqual(self.view(request).status_code, 200)

    def test_get_all_events_unauthenticated_status_code(self):
        request = self.factory.get('api/events/')

        self.assertEqual(self.view(request).status_code, 401)

    def test_create_valid_event_status_code(self):
        request = self.factory.post('api/events/', self.example, format='json')
        force_authenticate(request, user=self.user)

        assert self.view(request).status_code == 201

    def test_create_valid_event_is_in_db(self):

        request = self.factory.post('api/events/', self.example, format='json')
        force_authenticate(request, user=self.user)
        self.view(request)

        assert Event.objects.count() == 1

    def test_create_invalid_event(self):
        incorrect_example = self.example.copy()
        incorrect_example['name'] = '*'*100
        request = self.factory.post('api/events/', incorrect_example, format='json')
        force_authenticate(request, user=self.user)

        assert self.view(request).status_code == 400

    def test_create_unauthenticated_status_code(self):
        request = self.factory.post('api/events/', self.example, format='json')

        assert self.view(request).status_code == 401

    # def test_get_existing_event(self):
    #     event = EventFactory()
    #     url = f'api//events/{event.pk}/'
    #     request = self.factory.get(url)
    #     assert self.view(request).status_code == 200
    #
    # def test_get_non_existing_event(self):
    #     request = self.factory.get('api//events/test/')
    #     assert self.view(request).status_code == 404
    #
    # def test_update_event_with_valid_values(self):
    #     event = EventFactory()
    #     request = self.factory.put(f'api//events/{event.pk}/', self.example, format='json')
    #
    #     assert self.view(request).status_code == 200
    #
    # def test_update_event_with_invalid_value(self):
    #     event = EventFactory()
    #     incorrect_example = self.example.copy()
    #     incorrect_example['name'] = '*' * 100
    #     request = self.factory.put(f'api//events/{event.pk}/', incorrect_example, format='json')
    #
    #     assert self.view(request).status_code == 400
    #
    # def test_update_event_with_non_existing_address(self):
    #     event = EventFactory()
    #     incorrect_example = self.example.copy()
    #     incorrect_example['address']['country'] = ''
    #     incorrect_example['address']['city'] = ''
    #     incorrect_example['address']['street'] = ''
    #     incorrect_example['address']['number'] = ''
    #     request = self.factory.put(f'api//events/{event.pk}/', incorrect_example, format='json')
    #
    #     assert self.view(request).status_code == 400
    #
    # def test_update_event_with_valid_values_check_are_values_changed(self):
    #     event = EventFactory()
    #     request = self.factory.put(f'api//events/{event.pk}/', self.example, format='json')
    #     print(event)
    #     self.view(request)
    #     changed_event = Event.objects.get(pk=event.pk)
    #     print(changed_event)
    #     assert changed_event.name == self.example['name']
    #     assert changed_event.address.street == self.example['address']['street']
