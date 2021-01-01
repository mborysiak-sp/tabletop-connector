from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from rest_framework import filters

from tabletop_connector_api.events.models import Event
from tabletop_connector_api.events.utils import (
    address_to_geocode,
    get_distance_in_kilometers,
)
from tabletop_connector_api.users.models import User


def unpack_from_list(dictionary: dict, key):
    val = dictionary.get(key, None)
    if isinstance(val, list):
        dictionary[key] = dictionary.get(key)[0]


class FilterByParticipation(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user_pk = request.query_params.get("participant", None)
        print(user_pk)
        if not user_pk or not queryset:
            return queryset

        this_user = get_object_or_404(User, pk=user_pk)
        queryset = queryset.filter(participants=this_user)
        return queryset


class FilterByDistance(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        distance = request.query_params.get("distance", None)
        if not queryset or distance is None:
            return queryset

        distance = float(distance)
        geo_x = request.query_params.get("geo_x", None)
        geo_y = request.query_params.get("geo_y", None)

        if geo_x is None or geo_y is None:
            address_data = dict(request.query_params)
            for key in address_data:
                unpack_from_list(address_data, key)

            address_data.pop("distance", 0.0)
            geocode_from = address_to_geocode(address_data)
            if geocode_from == ():
                queryset = Event.objects.none()
                return queryset
            geo_x = geocode_from[0]
            geo_y = geocode_from[1]

        nearly_events = [
            x.id
            for x in queryset
            if get_distance_in_kilometers(
                x.address.geo_x, x.address.geo_y, float(geo_x), float(geo_y)
            )
            <= distance
        ]

        queryset = queryset.filter(id__in=nearly_events)
        return queryset


class FilterByDate(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if not queryset:
            return queryset

        date_from = request.query_params.get("date_from", None)
        date_to = request.query_params.get("date_to", None)
        now = datetime.now()
        if date_from is None:
            date_from = now
        else:
            try:
                date_from = datetime.strptime(date_from, "%Y-%m-%d")
                if date_from < datetime.now():
                    date_from = datetime.now()

            except ValueError:
                return queryset

        queryset = queryset.filter(date__gte=date_from)

        if date_to is None:
            return queryset

        try:
            date_to = datetime.strptime(date_to, "%Y-%m-%d")
            print(date_to)
            date_to = date_to + timedelta(days=1)
            print(date_to)

        except ValueError:
            return queryset

        queryset = queryset.filter(date__lt=date_to)
        return queryset
