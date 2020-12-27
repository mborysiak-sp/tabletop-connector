from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters, generics
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes
from rest_framework.generics import ListAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .filters import FilterByDistance, FilterByDate
from .models import Address, Event, Game
from .serializers import AddressSerializer, EventSerializer, EventCreateSerializer, AddressCreateSerializer, \
    GameSerializer


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    authentication_classes = ()
    permission_classes = ()
    queryset = Address.objects.all()

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update', 'create'):
            return AddressCreateSerializer
        return super().get_serializer_class()


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update', 'create'):
            return EventCreateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(creator=self.request.user, participants=[self.request.user, ])


class CustomEventAPIView(ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = EventSerializer
    model = serializer_class.Meta.model
    filter_backends = [filters.SearchFilter, FilterByDate, FilterByDistance, filters.OrderingFilter]
    search_fields = ['name', ]  # describe here which fields want to use for searching, then we use search=*
    ordering_fields = ['date', ]  # describe here which fields want to use for ordering, then we use order=(-)field

    def get_queryset(self):

        queryset = Event.objects.all()
        return queryset

    @action(detail=True)
    def list(self, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        if queryset.count() == 0:
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = self.serializer_class(queryset, many=True)
            page = self.paginate_queryset(queryset=serializer.data)

            return self.get_paginated_response(page)


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    filter_backends = [filters.SearchFilter]
    filter_class = Game
    search_fields = ['name']
    authentication_classes = ()
    permission_classes = ()


@api_view(['PATCH'])
def join_leave_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.user == event.creator:
        print(request.user == event.creator)
        return Response(None, status.HTTP_405_METHOD_NOT_ALLOWED)

    if request.user in event.participants.all():
        event.participants.remove(request.user)

    else:
        event.participants.add(request.user)

    event.save()
    return Response(None, status.HTTP_200_OK)
