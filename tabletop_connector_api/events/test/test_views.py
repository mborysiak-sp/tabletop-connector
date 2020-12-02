import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from tabletop_connector_api.events.models import Event
from tabletop_connector_api.events.serializers import EventSerializer
from tabletop_connector_api.events.test.factories import EventFactory, AddressFactory
from tabletop_connector_api.events.views import CustomEventViewSet, EventViewSet


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


# @pytest.mark.django_db
# class TestEventViewSet(TestCase):
#
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.view = EventViewSet.as_view({'get': 'list', 'post': 'create'})
#         self.example = {'name': 'test',
#                         'date': '2020-12-10T16:01:00+0000',
#                         'creator': 'null',
#                         'address': {
#                             'country': 'Poland',
#                             'city': 'Gdansk',
#                             'street': 'Wita Stwosza',
#                             'postal_code': '21-307',
#                             'number': '2',
#                             'geo_x': 'null',
#                             'geo_y': 'null'
#                         },
#                         'chat': 'null'}
#
#     def test_get_all_events(self):
#         EventFactory()
#         EventFactory(name='test2')
#         request = self.factory.get('api/event/')
#         events = Event.objects.all()
#         serializer = EventSerializer(events, many=True)
#         self.assertEqual(self.view(request).data['count'], len(serializer.data))
#
#     def test_create_valid_event(self):
#         request = self.factory.post('api/event/', self.example, format='json')
#
#
#         assert self.view(request).status_code == 200
#         assert Event.objects.count() == 1
#
#     def test_create_invalid_event(self):
#         incorrect_example = self.example.copy()
#         incorrect_example['name'] = '*'*100
#         request = self.factory.put('api/event/', incorrect_example, format='json')
#         assert Event.objects.count() == 0
