from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Profile
from .permissions import IsOwnerOrReadOnly, IsOwner
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
    permission_classes = (
        IsAuthenticated,
        IsOwner,
    )

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class TokenObtainView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        custom_response = {"auth_token": token.key, "user_id": user.id, "firstname": user.profile.firstname}
        return Response(custom_response)
