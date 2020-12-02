from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response

from .filters import FilterByDistance
from .models import Address, Event
from .serializers import AddressSerializer, EventSerializer


class AddressViewSet(viewsets.ViewSet):
    serializer_class = AddressSerializer
    authentication_classes = ()
    permission_classes = ()

    def list(self, request):
        serializer = self.serializer_class(Address.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        address = get_object_or_404(Address.objects.all(), pk=pk)
        return Response(self.serializer_class(address).data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        address = Address.objects.get(pk=pk)
        serializer = self.serializer_class(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        address = Address.objects.get(pk=pk)
        serializer = self.serializer_class(address, data=request.data)
        if serializer.is_valid():
            address.delete()
            return Response(serializer.data, status=status.HTTP_410_GONE)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventViewSet(viewsets.ViewSet):
    serializer_class = EventSerializer
    authentication_classes = ()
    permission_classes = ()

    def list(self, request):
        serializer = EventSerializer(Event.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        event = get_object_or_404(Event.objects.all(), pk=pk)
        return Response(self.serializer_class(event).data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        event = Event.objects.get(pk=pk)
        serializer = self.serializer_class(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        event = Event.objects.get(pk=pk)
        serializer = self.serializer_class(event, data=request.data)
        if serializer.is_valid():
            event.delete()
            return Response(serializer.data, status=status.HTTP_410_GONE)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
