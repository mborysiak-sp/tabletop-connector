from djoser.serializers import UserSerializer
from rest_framework import viewsets, mixins, views

from .models import User, Profile
from .permissions import IsUserOrReadOnly
from .serializers import ProfileSerializer


class ProfileViewSet(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsUserOrReadOnly,)
