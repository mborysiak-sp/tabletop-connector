from rest_framework import viewsets, status, filters
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .filters import FilterByDistance
from .models import Event, Address
from .serializers import AddressSerializer, EventSerializer, EventCreateSerializer, AddressCreateSerializer


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
        serializer.save(creator=self.request.user, participants=[self.request.user, ])

    # def list(self, request):
    #     serializer_class = self.serializer_class(Event.objects.all(), many=True)
    #     return Response(serializer_class.data, status=status.HTTP_200_OK)
    #
    # def create(self, request):
    #
    #     serializer_class = EventCreateSerializer(data=request.data)
    #     if serializer_class.is_valid():
    #         serializer_class.save()
    #         return Response(serializer_class.data, status=status.HTTP_201_CREATED)
    #
    #     return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    # def retrieve(self, request, pk=None):
    #
    #     event = get_object_or_404(Event.objects.all(), pk=pk)
    #
    #     return Response(self.serializer_class(event).data, status=status.HTTP_200_OK)
    #
    # def update(self, request, pk=None):
    #
    #     event = Event.objects.get(pk=pk)
    #     serializer = self.serializer_class(event, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def partial_update(self, request, pk=None):
    #     pass
    #
    # def destroy(self, request, pk=None):
    #
    #     event = Event.objects.get(pk=pk)                                     # also to remove then
    #     event.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class CustomEventViewSet(ListAPIView):

    authentication_classes = ()
    permission_classes = ()
    serializer_class = EventSerializer
    model = serializer_class.Meta.model
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):

        queryset = FilterByDistance().filter_queryset(self.request, self.queryset, self.__class__)
        return queryset

    def get(self, *args, **kwargs):

        queryset = self.get_queryset()
        if queryset.count() == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = self.serializer_class(queryset, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)




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
