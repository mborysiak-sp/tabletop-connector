from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import viewsets, mixins, views, status
from rest_framework.decorators import api_view
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


@api_view(['GET'])
def return_me(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    return Response(ProfileSerializer(user_profile, many=False).data, status.HTTP_200_OK)
