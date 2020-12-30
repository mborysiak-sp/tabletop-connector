from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, mixins, views, status
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser

from .models import User, Profile
from .permissions import IsUserOrReadOnly, IsOwnerOrReadOnly, IsOwner
from .serializers import ProfileSerializer, CreateProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """
    Updates and retrieves user accounts
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ("update", "partial_update", "create"):
            return CreateProfileSerializer
        return super().get_serializer_class()


class ProfileMeAPIView(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, IsOwner,)

    def get_object(self):
        return Profile.objects.get(user=self.request.user)
