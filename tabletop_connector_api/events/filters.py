import re
from abc import ABC
from datetime import datetime, timedelta

import pytz
from rest_framework import filters

from tabletop_connector_api.events.models import Event
from tabletop_connector_api.events.utils import address_to_geocode, get_distance_in_kilometers


class FilterByDistance(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):

        if not queryset:
            return queryset

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


class FilterByDate(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if not queryset:
            return queryset

        date_from = request.query_params.get('date_from', None)
        date_to = request.query_params.get('date_to', None)
        now = datetime.now()
        if date_from is None:
            date_from = now
        else:
            try:
                date_from = datetime.strptime(date_from, '%Y-%m-%d')
                if date_from < datetime.now():
                    date_from = datetime.now()



            except ValueError:
                return queryset

        queryset = queryset.filter(date__gte=date_from)

        if date_to is None:
            return queryset

        try:
            date_to = datetime.strptime(date_to, '%Y-%m-%d')
            print(date_to)
            date_to = date_to + timedelta(days=1)
            print(date_to)

        except ValueError:
            return queryset

        queryset = queryset.filter(date__lt=date_to)
        return queryset
