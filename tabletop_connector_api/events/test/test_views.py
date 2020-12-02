import pytest
from rest_framework.test import APIRequestFactory
from tabletop_connector_api.events.test.factories import EventFactory, AddressFactory
from tabletop_connector_api.events.views import CustomEventViewSet


@pytest.mark.django_db
class TestCustomEventViewSet:

    def test_CustomEventViewSet_found_response_code(self):
        view = CustomEventViewSet.as_view()
        factory = APIRequestFactory()
        EventFactory.create(address=AddressFactory(geo_x=54.34950, geo_y=18.64847))
        request = factory \
            .get('api/geteventbydistance/?distance=10&country=Poland&city=Gdansk&street=Teatralna')

        assert view(request).status_code == 302

    def test_CustomEventViewSet_found_in_queryset(self):
        view = CustomEventViewSet.as_view()
        factory = APIRequestFactory()
        EventFactory.create(address=AddressFactory(geo_x=54.34950, geo_y=18.64847))
        request = factory \
            .get('api/geteventbydistance/?distance=10&country=Poland&city=Gdansk&street=Teatralna')

        assert len(view(request).data) == 1

    def test_CustomEventViewSet_not_found_response_code(self):
        view = CustomEventViewSet.as_view()
        factory = APIRequestFactory()
        request = factory \
            .get('api/geteventbydistance/?distance=10&country=Poland&city=Gdansk&street=Teatralna')

        assert view(request).status_code == 404

    def test_CustomEventViewSet_when_address_no_specified(self):
        view = CustomEventViewSet.as_view()
        factory = APIRequestFactory()
        request = factory \
            .get('api/geteventbydistance/?distance=10')

        assert view(request).status_code == 404
