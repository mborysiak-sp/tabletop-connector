from datetime import datetime
from time import sleep

import pytest
import pytz
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate
from tabletop_connector_api.events.models import Event
from tabletop_connector_api.events.serializers import EventSerializer, AddressSerializer, AddressCreateSerializer
from tabletop_connector_api.events.test.factories import EventFactory, AddressFactory, UserFactory
from tabletop_connector_api.events.views import CustomEventAPIView, EventViewSet, AddressViewSet, join_leave_event


@pytest.mark.django_db
class TestCustomEventViewSet(TestCase):

    @pytest.fixture(autouse=True)
    def delay(self):
        sleep(1)

    def setUp(self):
        self.view = CustomEventAPIView.as_view()
        self.factory = APIRequestFactory()

    def test_serializer_class(self):
        self.assertEqual(CustomEventAPIView.serializer_class, EventSerializer)

    def test_found_response_code(self):
        EventFactory(address=AddressFactory(geo_x=54.34950,
                                            geo_y=18.64847))
        request = self.factory \
            .get('api/geteventbydistance/?distance=10&country=Poland&city=Gdansk&street=Teatralna')

        assert self.view(request).status_code == 200

    def test_found_in_queryset(self):
        EventFactory(address=AddressFactory(geo_x=54.34950,
                                            geo_y=18.64847))

        EventFactory(address=AddressFactory(city='Wroclaw',
                                            street='Sanocka',
                                            number='9',
                                            geo_x=51.09421,
                                            geo_y=17.02858))
        request = self.factory \
            .get('api/geteventbydistance/?distance=10&country=Poland&city=Gdansk&street=Teatralna')

        assert self.view(request).data.get('count') == 1

    def test_not_found_response_code(self):
        EventFactory(address=AddressFactory(city='Wroclaw',
                                            street='Sanocka',
                                            number='9',
                                            geo_x=51.09421,
                                            geo_y=17.02858))
        request = self.factory \
            .get('api/geteventbydistance/?distance=10&country=Poland&city=Gdansk&street=Teatralna')

        assert self.view(request).status_code == 204

    def test_when_address_no_specified(self):
        EventFactory(address=AddressFactory(city='Wroclaw',
                                            street='Sanocka',
                                            number='9'))
        request = self.factory \
            .get('api/geteventbydistance/?distance=10')

        assert self.view(request).status_code == 204

    def test_search(self):
        EventFactory(address=AddressFactory(geo_x=54.34950,
                                            geo_y=18.64847))

        EventFactory(name='xyz',
                     address=AddressFactory(geo_x=54.34950,
                                            geo_y=18.64847))
        request = self.factory \
            .get('api/geteventbydistance/?search=x&distance=10&country=Poland&city=Gdansk&street=Teatralna')

        assert self.view(request).data.get('count') == 1

    def test_with_date_from_found(self):
        EventFactory(address=AddressFactory(geo_x=54.34950,
                                            geo_y=18.64847))
        EventFactory(date=datetime(2010, 12, 25, 11, 0, tzinfo=pytz.UTC),
                     address=AddressFactory(geo_x=54.34950,
                                            geo_y=18.64847))
        request = self.factory \
            .get('api/geteventbydistance/?distance=10&country=Poland&city=Gdansk&street=Teatralna&date_from=2011-1-1')

        assert self.view(request).data.get('count') == 1

    def test_with_date_from_not_found(self):
        EventFactory(date=datetime(2010, 12, 25, 11, 0, tzinfo=pytz.UTC), address=AddressFactory(geo_x=54.34950,
                                            geo_y=18.64847))
        request = self.factory \
            .get('api/geteventbydistance/?distance=10&country=Poland&city=Gdansk&street=Teatralna&date_from=2031-1-1')

        assert not self.view(request).data

    def test_with_date_to_found(self):
        EventFactory(address=AddressFactory(geo_x=54.34950,
                                            geo_y=18.64847))
        EventFactory(date=datetime(2032, 12, 25, 11, 0, tzinfo=pytz.UTC),
                     address=AddressFactory(
                         geo_x=54.34950,
                         geo_y=18.64847))
        request = self.factory \
            .get('api/geteventbydistance/?distance=10&country=Poland&city=Gdansk&street=Teatralna&date_to=2031-1-1')

        assert self.view(request).data.get('count') == 1

    def test_with_date_to_not_found(self):
        EventFactory(address=AddressFactory(geo_x=54.34950,
                                            geo_y=18.64847))
        request = self.factory \
            .get('api/geteventbydistance/?distance=10&country=Poland&city=Gdansk&street=Teatralna&date_to=2011-1-1')

        assert not self.view(request).data

    def test_with_date_from_and_date_to_found(self):
        EventFactory(address=AddressFactory(geo_x=54.34950,
                                            geo_y=18.64847))
        EventFactory(date=datetime(2032, 12, 25, 11, 0, tzinfo=pytz.UTC),
                     address=AddressFactory(
                         geo_x=54.34950,
                         geo_y=18.64847))
        request = self.factory \
            .get('api/geteventbydistance/'
                 '?distance=10&country=Poland&city=Gdansk&street=Teatralna&date_from=2020-1-1&date_to=2031-1-1')

        assert self.view(request).data.get('count') == 1


@pytest.mark.django_db
class TestAddressViewSet(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_get_serializer_class(self):
        request = self.factory.get(reverse('events:address-list'))
        v = AddressViewSet()
        v.action = 'list'

        assert v.get_serializer_class() == AddressSerializer

    def test_get_serializer_class_when_any_changes(self):
        v = AddressViewSet()
        v.action = 'update'

        assert v.get_serializer_class() == AddressCreateSerializer


@pytest.mark.django_db
class TestEventViewSet(TestCase):

    @pytest.fixture(autouse=True)
    def reset(self):
        self.view = EventViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'})
        sleep(1)

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory()
        self.example = {'name': 'test',
                        'date': '2020-12-14T20:09:00+0000',
                        'creator': None,
                        'address': {
                            'country': 'Poland',
                            'city': 'Gdansk',
                            'street': 'Wita Stwosza',
                            'postal_code': '21-307',
                            'number': '2',
                            'geo_x': None,
                            'geo_y': None
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
        request = self.factory.get(reverse('events:event-list'))
        force_authenticate(request, user=self.user)

        self.assertEqual(self.view(request).status_code, 200)

    def test_get_all_events_unauthenticated_status_code(self):
        request = self.factory.get(reverse('events:event-list'))

        self.assertEqual(self.view(request).status_code, 401)

    def test_create_valid_event_status_code(self):
        request = self.factory.post(reverse('events:event-list'), self.example, format='json')
        force_authenticate(request, user=self.user)

        assert self.view(request).status_code == 201

    def test_create_valid_event_is_in_db(self):
        request = self.factory.post(reverse('events:event-list'), self.example, format='json')
        force_authenticate(request, user=self.user)
        self.view(request)

        assert Event.objects.count() == 1

    def test_create_valid_event_creator_is_participant(self):
        example_with_creator = self.example.copy()
        example_with_creator['creator'] = self.user.pk
        request = self.factory.post(reverse('events:event-list'), self.example, format='json')
        force_authenticate(request, user=self.user)
        self.view(request)

        assert self.user in Event.objects.get(creator=self.user.pk).participants.all()

    def test_create_invalid_event(self):
        incorrect_example = self.example.copy()
        incorrect_example['name'] = '*'*100
        request = self.factory.post(reverse('events:event-list'), incorrect_example, format='json')
        force_authenticate(request, user=self.user)

        assert self.view(request).status_code == 400

    def test_create_unauthenticated_status_code(self):
        request = self.factory.post(reverse('events:event-list'), self.example, format='json')

        assert self.view(request).status_code == 401

    def test_get_existing_event(self):
        event = EventFactory()
        self.view = EventViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(reverse('events:event-list'))
        force_authenticate(request, user=self.user)

        assert self.view(request, pk=event.pk).status_code == 200

    def test_get_not_existing_event(self):
        self.view = EventViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(reverse('events:event-list'))
        force_authenticate(request, user=self.user)

        assert self.view(request, pk='xD').status_code == 404

    def test_get_event_unauthenticated(self):
        event = EventFactory()
        self.view = EventViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(reverse('events:event-list'))

        assert self.view(request, pk=event.pk).status_code == 401

    def test_update_event_with_valid_values(self):
        event = EventFactory()
        request = self.factory.put(reverse('events:event-list'), self.example, format='json')
        force_authenticate(request, user=self.user)

        assert self.view(request, pk=event.pk).status_code == 200

    def test_update_event_with_invalid_value(self):
        event = EventFactory()
        incorrect_example = self.example.copy()
        incorrect_example['name'] = '*' * 100
        request = self.factory.put('api/events/', incorrect_example, format='json')
        force_authenticate(request, user=self.user)

        assert self.view(request, pk=event.pk).status_code == 400

    def test_update_event_with_not_existing_address(self):
        event = EventFactory()
        incorrect_example = self.example.copy()
        incorrect_example['address']['country'] = ''
        incorrect_example['address']['city'] = ''
        incorrect_example['address']['street'] = ''
        incorrect_example['address']['number'] = ''
        request = self.factory.put(reverse('events:event-list'), incorrect_example, format='json')
        force_authenticate(request, user=self.user)

        assert self.view(request, pk=event.pk).status_code == 400

    def test_update_event_with_valid_values_check_are_values_changed(self):
        event = EventFactory()
        request = self.factory.put(reverse('events:event-list'), self.example, format='json')
        force_authenticate(request, user=self.user)
        self.view(request, pk=event.pk)
        changed_event = Event.objects.get(pk=event.pk)

        assert changed_event.name == self.example['name']
        assert changed_event.address.street == self.example['address']['street']

    def test_update_event_unauthenticated(self):
        event = EventFactory()
        request = self.factory.put(reverse('events:event-list'), self.example, format='json')

        assert self.view(request, pk=event.pk).status_code == 401

    def test_destroy_existing_event_code(self):
        event = EventFactory()
        request = self.factory.delete(reverse('events:event-list'))
        force_authenticate(request, user=self.user)

        assert self.view(request, pk=event.pk).status_code == 204

    def test_destroy_existing_event_is_not_in_db(self):
        event = EventFactory()
        request = self.factory.delete(reverse('events:event-list'))
        force_authenticate(request, user=self.user)
        self.view(request, pk=event.pk)

        self.assertEqual(Event.objects.count(), 0)

    def test_destroy_not_existing_event_code(self):
        request = self.factory.delete(reverse('events:event-list'))
        force_authenticate(request, user=self.user)

        assert self.view(request, pk='xD').status_code == 404

    def test_destroy_unauthenticated(self):
        event = EventFactory()
        request = self.factory.delete(reverse('events:event-list'))

        assert self.view(request, pk=event.pk).status_code == 401


@pytest.mark.django_db
class TestJoinLeaveEvent(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory(username='test')
        self.user_2 = UserFactory(username='xd')
        self.view = join_leave_event

    def test_if_joined_not_creator(self):
        event = EventFactory(creator=self.user)
        request = self.factory.patch('api/participation/')
        force_authenticate(request, user=self.user_2)
        assert self.view(request, pk=event.pk).status_code == 200

    def test_if_joined_not_creator_in_participants(self):
        event = EventFactory(creator=self.user)
        request = self.factory.patch('api/participation/')
        force_authenticate(request, user=self.user_2)
        self.view(request, pk=event.pk)

        assert self.user_2 in event.participants.all()

    def test_if_left_not_creator(self):
        event = EventFactory(creator=self.user)
        event.participants.add(self.user_2)
        request = self.factory.patch('api/participation/')
        force_authenticate(request, user=self.user_2)
        assert self.view(request, pk=event.pk).status_code == 200

    def test_if_left_not_creator_not_in_participants(self):
        event = EventFactory(creator=self.user)
        event.participants.add(self.user_2)
        request = self.factory.patch('api/participation/')
        force_authenticate(request, user=self.user_2)
        self.view(request, pk=event.pk)
        assert self.user_2 not in event.participants.all()

    def test_if_owner(self):
        event = EventFactory(creator=self.user)
        request = self.factory.patch('api/participation/')
        force_authenticate(request, user=self.user)

        assert self.view(request, pk=event.pk).status_code == 405

    def test_if_no_event_found(self):
        request = self.factory.patch('api/participation/')
        force_authenticate(request, user=self.user)
        assert self.view(request, pk='123e4567-e89b-12d3-a456-426614174000').status_code == 404
