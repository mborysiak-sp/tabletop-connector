from abc import ABC

from rest_framework import filters

from tabletop_connector_api.events.models import Event
from tabletop_connector_api.events.utils import address_to_geocode, get_distance_in_kilometers


class FilterByDistance(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        distance = float(request.query_params.get('distance', 0.0))
        address_data = dict(request.query_params)
        address_data.pop('distance', 0.0)
        geocode_from = address_to_geocode(address_data)
        if geocode_from == ():
            queryset = Event.objects.none()
            return queryset

        nearly_events = [x.id for x in queryset if get_distance_in_kilometers(x.address.geo_x,
                                                                              x.address.geo_y,
                                                                              geocode_from[0],
                                                                              geocode_from[1]) < distance]
        queryset = queryset.filter(id__in=nearly_events)
        return queryset
