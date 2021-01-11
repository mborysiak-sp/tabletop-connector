from rest_framework import viewsets

from .models import Chat
from .serializers import ChatSerializer


class ChatModelViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()
