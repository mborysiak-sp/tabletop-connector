from djoser.serializers import UserSerializer
from rest_framework import viewsets, mixins, views
from rest_framework.parsers import MultiPartParser

from .models import User, Profile
from .permissions import IsUserOrReadOnly, IsOwnerOrReadOnly
from .serializers import ProfileSerializer, CreateProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """
    Updates and retrieves user accounts
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update', 'create'):
            return CreateProfileSerializer
        return super().get_serializer_class()
