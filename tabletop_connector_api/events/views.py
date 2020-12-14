from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters, generics
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes
from rest_framework.generics import ListAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response

from .filters import FilterByDistance
from .models import Address, Event, Game
from .serializers import AddressSerializer, EventSerializer, EventCreateSerializer, AddressCreateSerializer, GameSerializer


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
    authentication_classes = ()
    permission_classes = ()

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update', 'create'):
            return EventCreateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user, participants=[self.request.user, ])


class CustomEventAPIView(ListAPIView):

    authentication_classes = ()
    permission_classes = ()
    serializer_class = EventSerializer
    model = serializer_class.Meta.model
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):

        queryset = FilterByDistance().filter_queryset(self.request, self.queryset, self.__class__)
        return queryset

    @action(detail=True)
    def get(self, *args, **kwargs):

        queryset = self.get_queryset()
        if queryset.count() == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = self.serializer_class(queryset, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    filter_backends = [filters.SearchFilter]
    filter_class = Game
    search_fields = ['name']
    authentication_classes = ()
    permission_classes = ()


@api_view(['PATCH'])
@permission_classes(())
@authentication_classes(())
def join_leave_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.user in event.participants:
        event.participants.remove(request.user)

    else:
        event.participants.add(request.user)

    event.save()
    return Response(status.HTTP_200_OK)
