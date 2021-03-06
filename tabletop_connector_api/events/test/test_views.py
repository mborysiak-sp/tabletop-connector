from datetime import datetime

import pytest
import pytz
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate

from tabletop_connector_api.events.models import Event
from tabletop_connector_api.events.serializers import (
    EventSerializer,
    AddressSerializer,
    AddressCreateSerializer,
)
from tabletop_connector_api.events.test.factories import (
    EventFactory,
    AddressFactory,
    UserFactory, GameFactory,
)
from tabletop_connector_api.events.views import (
    CustomEventAPIView,
    EventViewSet,
    AddressViewSet,
    join_leave_event,
)


@pytest.mark.django_db
class TestCustomEventViewSet(TestCase):

    # @pytest.fixture(autouse=True)
    # def delay(self):
    #     sleep(1)

    def setUp(self):
        self.view = CustomEventAPIView.as_view()
        self.factory = APIRequestFactory()
        self.user = UserFactory(username="bambo")

    def test_serializer_class(self):
        self.assertEqual(CustomEventAPIView.serializer_class, EventSerializer)

    def test_found_response_code(self):
        EventFactory(address=AddressFactory(geo_x=54.34950, geo_y=18.64847))
        request = self.factory.get(
            "events/search/?distance=10&country=Poland&city=Gdansk&street=Teatralna"
        )
        force_authenticate(request, user=self.user)

        assert self.view(request).status_code == 200

    def test_found_in_queryset(self):
        EventFactory(address=AddressFactory(geo_x=54.34950, geo_y=18.64847))

        EventFactory(
            address=AddressFactory(
                city="Wroclaw",
                street="Sanocka",
                number="9",
                geo_x=51.09421,
                geo_y=17.02858,
            )
        )
        request = self.factory.get(
            "events/search/?distance=10&country=Poland&city=Gdansk&street=Teatralna"
        )
        force_authenticate(request, user=self.user)

        assert self.view(request).data.get("count") == 1

    def test_found_by_geocode_in_queryset(self):
        EventFactory(address=AddressFactory(geo_x=54.34950, geo_y=18.64847))

        EventFactory(
            address=AddressFactory(
                city="Wroclaw",
                street="Sanocka",
                number="9",
                geo_x=51.09421,
                geo_y=17.02858,
            )
        )
        request = self.factory.get(
            "events/search/?distance=10&geo_x=51.09421&geo_y=17.02858"
        )
        force_authenticate(request, user=self.user)

        assert self.view(request).data.get("count") == 1

    def test_not_found_by_geocode_in_queryset(self):
        EventFactory(address=AddressFactory(geo_x=54.34950, geo_y=18.64847))

        EventFactory(
            address=AddressFactory(
                city="Wroclaw",
                street="Sanocka",
                number="9",
                geo_x=51.09421,
                geo_y=17.02858,
            )
        )
        request = self.factory.get("events/search/?distance=10&geo_x=1.0&geo_y=1.0")
        force_authenticate(request, user=self.user)

        assert self.view(request).data.get("count") == 0

    def test_not_found_response_code(self):
        EventFactory(
            address=AddressFactory(
                city="Wroclaw",
                street="Sanocka",
                number="9",
                geo_x=51.09421,
                geo_y=17.02858,
            )
        )
        request = self.factory.get(
            "events/search/?distance=10&country=Poland&city=Gdansk&street=Teatralna"
        )
        force_authenticate(request, user=self.user)

        assert self.view(request).status_code == 200

    def test_when_no_distance_specified(self):
        EventFactory(
            address=AddressFactory(city="Wroclaw", street="Sanocka", number="9")
        )
        request = self.factory.get(
            "events/search/?country=Poland&city=Gdansk&street=Teatralna"
        )
        force_authenticate(request, user=self.user)
        assert self.view(request).data.get("count") == 1

    def test_when_address_no_specified(self):
        EventFactory(
            address=AddressFactory(city="Wroclaw", street="Sanocka", number="9")
        )
        request = self.factory.get("events/search/?distance=10")
        force_authenticate(request, user=self.user)

        assert self.view(request).status_code == 200

    def test_search(self):
        EventFactory(address=AddressFactory(geo_x=54.34950, geo_y=18.64847))

        EventFactory(name="xyz", address=AddressFactory(geo_x=54.34950, geo_y=18.64847))
        request = self.factory.get(
            "events/search/?search=x&distance=10&country=Poland&city=Gdansk&street=Teatralna"
        )
        force_authenticate(request, user=self.user)

        assert self.view(request).data.get("count") == 1

    def test_search_by_game_name(self):
        EventFactory(address=AddressFactory(geo_x=54.34950, geo_y=18.64847))

        ev = EventFactory(address=AddressFactory(geo_x=54.34950, geo_y=18.64847))
        ev.games.add(GameFactory())
        request = self.factory.get(
            "events/search/?search=qq&distance=10&country=Poland&city=Gdansk&street=Teatralna"
        )
        force_authenticate(request, user=self.user)

        assert self.view(request).data.get("count") == 1

    def test_with_date_from_found(self):

        EventFactory(address=AddressFactory(geo_x=54.34950, geo_y=18.64847))
        EventFactory(
            date=datetime(2010, 12, 25, 11, 0, tzinfo=pytz.UTC),
            address=AddressFactory(geo_x=54.34950, geo_y=18.64847),
        )
        request = self.factory.get(
            "events/search/?distance=10&country=Poland&city=Gdansk&street=Teatralna&date_from=2011-1-1"
        )
        force_authenticate(request, user=self.user)

        assert self.view(request).data.get("count") == 1

    def test_with_date_from_not_found(self):
        EventFactory(
            date=datetime(2010, 12, 25, 11, 0, tzinfo=pytz.UTC),
            address=AddressFactory(geo_x=54.34950, geo_y=18.64847),
        )
        request = self.factory.get(
            "events/search/?distance=10&country=Poland&city=Gdansk&street=Teatralna&date_from=2031-1-1"
        )
        force_authenticate(request, user=self.user)

        assert self.view(request).data.get("count") == 0

    def test_with_date_to_found(self):
        EventFactory(address=AddressFactory(geo_x=54.34950, geo_y=18.64847))
        EventFactory(
            date=datetime(2032, 12, 25, 11, 0, tzinfo=pytz.UTC),
            address=AddressFactory(geo_x=54.34950, geo_y=18.64847),
        )
        request = self.factory.get(
            "events/search/?distance=10&country=Poland&city=Gdansk&street=Teatralna&date_to=2031-1-1"
        )
        force_authenticate(request, user=self.user)

        assert self.view(request).data.get("count") == 1

    def test_with_date_to_not_found(self):
        EventFactory(address=AddressFactory(geo_x=54.34950, geo_y=18.64847))
        request = self.factory.get(
            "events/search/?distance=10&country=Poland&city=Gdansk&street=Teatralna&date_to=2011-1-1"
        )
        force_authenticate(request, user=self.user)

        assert self.view(request).data.get("count") == 0

    def test_with_date_from_and_date_to_found(self):
        EventFactory(address=AddressFactory(geo_x=54.34950, geo_y=18.64847))
        EventFactory(
            date=datetime(2032, 12, 25, 11, 0, tzinfo=pytz.UTC),
            address=AddressFactory(geo_x=54.34950, geo_y=18.64847),
        )
        request = self.factory.get(
            "events/search/"
            "?distance=10&country=Poland&city=Gdansk&street=Teatralna&date_from=2020-1-1&date_to=2031-1-1"
        )
        force_authenticate(request, user=self.user)

        assert self.view(request).data.get("count") == 1

    def test_by_geocode(self):
        EventFactory(address=AddressFactory(geo_x=54.34950, geo_y=18.64847))
        EventFactory(address=AddressFactory(geo_x=54.34950, geo_y=21.64847))
        request = self.factory.get(
            "events/search/" "?distance=10&geo_x=54.34950&geo_y=18.64847"
        )
        force_authenticate(request, user=self.user)

        assert self.view(request).data.get("count") == 1

    def test_by_participant(self):
        usr1 = UserFactory()
        usr2 = UserFactory(username="xd")
        usr3 = UserFactory(username="xd2")
        ev1 = EventFactory(address=AddressFactory(geo_x=54.34950, geo_y=18.64847))
        ev2 = EventFactory(address=AddressFactory(geo_x=54.34950, geo_y=21.64847))
        ev3 = EventFactory(address=AddressFactory(geo_x=54.34950, geo_y=21.64847))
        ev1.participants.add(usr1)
        ev3.participants.add(usr1, usr3)
        ev2.participants.add(usr2)

        request = self.factory.get("events/search/" f"?participant={usr1.pk}")
        force_authenticate(request, user=self.user)
        assert self.view(request).data.get("count") == 2

    def test_by_not_existing_participant(self):
        EventFactory(address=AddressFactory(geo_x=54.34950, geo_y=18.64847))
        request = self.factory.get(
            "events/search/" "?participant=123e4567-e89b-12d3-a456-426614174000"
        )
        force_authenticate(request, user=self.user)
        assert self.view(request).status_code == 404

    def test_all_query_params(self):
        usr1 = UserFactory()
        ev = EventFactory(address=AddressFactory(geo_x=54.34950, geo_y=18.64847))
        EventFactory(name="xd", address=AddressFactory(geo_x=54.34950, geo_y=18.64847))
        ev.participants.add(usr1)
        request = self.factory.get(
            "events/search/"
            "?distance=10&geo_x=54.34950&geo_y=18.64847"
            f"&participant={usr1.pk}"
            "&search=test"
            "&date_from=2020-1-1&date_to=2031-1-1"
        )
        force_authenticate(request, user=self.user)
        assert self.view(request).data.get("count") == 1


@pytest.mark.django_db
class TestAddressViewSet(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_get_serializer_class(self):
        request = self.factory.get(reverse("events:address-list"))
        v = AddressViewSet()
        v.action = "list"

        assert v.get_serializer_class() == AddressSerializer

    def test_get_serializer_class_when_any_changes(self):
        v = AddressViewSet()
        v.action = "update"

        assert v.get_serializer_class() == AddressCreateSerializer


@pytest.mark.django_db
class TestEventViewSet(TestCase):
    @pytest.fixture(autouse=True)
    def reset(self):
        self.view = EventViewSet.as_view(
            {"get": "list", "post": "create", "put": "update", "delete": "destroy"}
        )
        # sleep(1)

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory()
        self.example = {
            "name": "TEST 1",
            "date": "2020-12-30T16:01:00+0000",
            "address": {"geo_x": 54.395704550000005, "geo_y": 18.5739726651911},
            "games": [],
        }

    def test_get_all_events(self):
        EventFactory()
        EventFactory(name="test2")
        request = self.factory.get("api/events/")
        force_authenticate(request, user=self.user)
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        self.assertEqual(self.view(request).data["results"], serializer.data)

    def test_get_all_events_status_code(self):
        EventFactory()
        EventFactory(name="test2")
        request = self.factory.get(reverse("events:event-list"))
        force_authenticate(request, user=self.user)

        self.assertEqual(self.view(request).status_code, 200)

    def test_get_all_events_unauthenticated_status_code(self):
        request = self.factory.get(reverse("events:event-list"))

        self.assertEqual(self.view(request).status_code, 401)

    def test_create_valid_event_status_code(self):
        request = self.factory.post(
            reverse("events:event-list"), self.example, format="json"
        )
        force_authenticate(request, user=self.user)

        assert self.view(request).status_code == 201

    def test_create_valid_event_is_in_db(self):
        request = self.factory.post(
            reverse("events:event-list"), self.example, format="json"
        )
        force_authenticate(request, user=self.user)
        self.view(request)

        assert Event.objects.count() == 1

    def test_create_valid_event_creator_is_participant(self):
        request = self.factory.post(
            reverse("events:event-list"), self.example, format="json"
        )
        force_authenticate(request, user=self.user)
        self.view(request)

        assert self.user in Event.objects.get(creator=self.user.pk).participants.all()

    def test_create_invalid_event(self):
        incorrect_example = self.example.copy()
        incorrect_example["name"] = "*" * 100
        request = self.factory.post(
            reverse("events:event-list"), incorrect_example, format="json"
        )
        force_authenticate(request, user=self.user)

        assert self.view(request).status_code == 400

    def test_create_unauthenticated_status_code(self):
        request = self.factory.post(
            reverse("events:event-list"), self.example, format="json"
        )

        assert self.view(request).status_code == 401

    def test_get_existing_event(self):
        event = EventFactory()
        self.view = EventViewSet.as_view({"get": "retrieve"})
        request = self.factory.get(reverse("events:event-list"))
        force_authenticate(request, user=self.user)

        assert self.view(request, pk=event.pk).status_code == 200

    def test_get_not_existing_event(self):
        self.view = EventViewSet.as_view({"get": "retrieve"})
        request = self.factory.get(reverse("events:event-list"))
        force_authenticate(request, user=self.user)

        assert self.view(request, pk="xD").status_code == 404

    def test_get_event_unauthenticated(self):
        event = EventFactory()
        self.view = EventViewSet.as_view({"get": "retrieve"})
        request = self.factory.get(reverse("events:event-list"))

        assert self.view(request, pk=event.pk).status_code == 401

    def test_update_event_with_valid_values(self):
        event = EventFactory()
        request = self.factory.put(
            reverse("events:event-list"), self.example, format="json"
        )
        force_authenticate(request, user=self.user)

        assert self.view(request, pk=event.pk).status_code == 200

    def test_update_event_with_invalid_value(self):
        event = EventFactory()
        incorrect_example = self.example.copy()
        incorrect_example["name"] = "*" * 100
        request = self.factory.put("api/events/", incorrect_example, format="json")
        force_authenticate(request, user=self.user)

        assert self.view(request, pk=event.pk).status_code == 400

    def test_update_event_with_not_existing_address(self):
        event = EventFactory()
        incorrect_example = self.example.copy()
        incorrect_example["address"]["geo_x"] = 1000
        incorrect_example["address"]["geo_y"] = 1000

        request = self.factory.put(
            reverse("events:event-list"), incorrect_example, format="json"
        )
        force_authenticate(request, user=self.user)

        assert self.view(request, pk=event.pk).status_code == 400

    def test_update_event_with_valid_values_check_are_values_changed(self):
        event = EventFactory()
        request = self.factory.put(
            reverse("events:event-list"), self.example, format="json"
        )
        force_authenticate(request, user=self.user)
        self.view(request, pk=event.pk)
        changed_event = Event.objects.get(pk=event.pk)

        assert changed_event.name == self.example["name"]
        assert changed_event.address.geo_x == self.example["address"]["geo_x"]

    def test_update_event_unauthenticated(self):
        event = EventFactory()
        request = self.factory.put(
            reverse("events:event-list"), self.example, format="json"
        )

        assert self.view(request, pk=event.pk).status_code == 401

    def test_destroy_existing_event_code(self):
        event = EventFactory()
        request = self.factory.delete(reverse("events:event-list"))
        force_authenticate(request, user=self.user)

        assert self.view(request, pk=event.pk).status_code == 204

    def test_destroy_existing_event_is_not_in_db(self):
        event = EventFactory()
        request = self.factory.delete(reverse("events:event-list"))
        force_authenticate(request, user=self.user)
        self.view(request, pk=event.pk)

        self.assertEqual(Event.objects.count(), 0)

    def test_destroy_not_existing_event_code(self):
        request = self.factory.delete(reverse("events:event-list"))
        force_authenticate(request, user=self.user)

        assert self.view(request, pk="xD").status_code == 404

    def test_destroy_unauthenticated(self):
        event = EventFactory()
        request = self.factory.delete(reverse("events:event-list"))

        assert self.view(request, pk=event.pk).status_code == 401

    def test_chat_not_null_when_event_created(self):
        request = self.factory.post(
            reverse("events:event-list"), self.example, format="json"
        )
        force_authenticate(request, user=self.user)
        self.view(request)

        assert Event.objects.get(creator=self.user.pk).chat is not None

    def test_creator_as_chat_participant(self):
        request = self.factory.post(
            reverse("events:event-list"), self.example, format="json"
        )
        force_authenticate(request, user=self.user)
        self.view(request)

        assert (
            self.user in Event.objects.get(creator=self.user.pk).chat.participants.all()
        )


@pytest.mark.django_db
class TestJoinLeaveEvent(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory(username="test")
        self.user_2 = UserFactory(username="xd")
        self.view = join_leave_event

    def test_if_joined_not_creator(self):
        event = EventFactory(creator=self.user)
        request = self.factory.patch("api/participation/")
        force_authenticate(request, user=self.user_2)

        assert self.view(request, pk=event.pk).status_code == 200

    def test_if_joined_participant_in_participants_and_chat(self):
        event = EventFactory(creator=self.user)
        request = self.factory.patch("api/participation/")
        force_authenticate(request, user=self.user_2)
        self.view(request, pk=event.pk)

        assert self.user_2 in event.participants.all()
        assert self.user_2 in event.chat.participants.all()

    def test_if_left_participant(self):
        event = EventFactory(creator=self.user)
        event.participants.add(self.user_2)
        request = self.factory.patch("api/participation/")
        force_authenticate(request, user=self.user_2)

        assert self.view(request, pk=event.pk).status_code == 200

    def test_if_left_not_creator_not_in_participants_and_chat(self):
        event = EventFactory(creator=self.user)
        event.participants.add(self.user_2)
        request = self.factory.patch("api/participation/")
        force_authenticate(request, user=self.user_2)
        self.view(request, pk=event.pk)

        assert self.user_2 not in event.participants.all()
        assert self.user_2 not in event.chat.participants.all()

    def test_if_owner_status_code(self):
        event = EventFactory(creator=self.user)
        request = self.factory.patch("api/participation/")
        force_authenticate(request, user=self.user)

        assert self.view(request, pk=event.pk).status_code == 405

    def test_if_no_event_found(self):
        request = self.factory.patch("api/participation/")
        force_authenticate(request, user=self.user)
        assert (
            self.view(request, pk="123e4567-e89b-12d3-a456-426614174000").status_code
            == 404
        )
