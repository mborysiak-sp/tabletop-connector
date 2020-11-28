# Create your views here.

from rest_framework import viewsets, generics, mixins, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .filters import FilterByDistance
from .models import Address, Event
from .serializers import AddressSerializer, EventSerializer
from .utils import address_to_geocode, get_distance_in_kilometers


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = ()
    permission_classes = ()


class CustomEventViewSet(ListAPIView):
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

    # def list(self, request):
    # events = Event.objects.all()
    # serializer = EventSerializer(events, many=True)
    # return Response(serializer.data)

    # def create(self, request):
    #     serializer = EventSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def retrieve(self, request, pk=None):
    #     queryset = Event.objects.all()
    #     event = get_object_or_404(queryset, pk=pk)
    #     serializer = EventSerializer(event)
    #     return Response(serializer.data)
    #
    # def update(self, request, pk=None):
    #     event = Event.objects.get(pk=pk)
    #     serializer = EventSerializer(event, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def partial_update(self, request, pk=None):
    #     pass
    #
    # def destroy(self, request, pk=None):
    #     event = Event.objects.get(pk=pk)
    #     serializer = EventSerializer(event, data=request.data)
    #     if serializer.is_valid():
    #         event.delete()
    #         return Response(serializer.data, status=status.HTTP_410_GONE)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
