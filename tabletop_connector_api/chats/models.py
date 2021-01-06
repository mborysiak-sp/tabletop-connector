import uuid

from django.db import models

from ..users.models import User


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, blank=True, related_name="chats")


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    handle = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    content = models.TextField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)
