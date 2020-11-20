from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import User, Event, Address
from .permissions import IsUserOrReadOnly
from .serializers import CreateUserSerializer, UserSerializer, EventSerializer, AddressSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly,)


class UserCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    Creates user accounts
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer



class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (AllowAny,)

    #def list(self, request):
        #events = Event.objects.all()
        #serializer = EventSerializer(events, many=True)
        #return Response(serializer.data)

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