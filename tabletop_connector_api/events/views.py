from rest_framework import filters
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .filters import FilterByDistance
from .models import Address, Event, Game
from .serializers import AddressSerializer, EventSerializer, GameSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = ()
    permission_classes = ()


class CustomEventAPIView(ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = EventSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):

        queryset = FilterByDistance().filter_queryset(self.request, self.queryset, self.__class__)

        return queryset

    def get(self, *args, **kwargs):

        queryset = self.get_queryset()
        if queryset.count() == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(queryset, many=True)
            return Response(data=serializer.data, status=status.HTTP_302_FOUND)


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    filter_backends = [filters.SearchFilter]
    filter_class = Game
    search_fields = ['name']
    authentication_classes = ()
    permission_classes = ()