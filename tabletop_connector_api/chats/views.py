from rest_framework import permissions
from rest_framework import viewsets

from .serializers import ChatSerializer


class ChatModelViewSet(viewsets.ModelViewSet):
    permission_classes = permissions.IsAdminUser
    serializer_class = ChatSerializer
