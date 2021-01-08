from rest_framework import permissions
from rest_framework import viewsets

from .serializers import ChatSerializer


class ChatModelViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSerializer

