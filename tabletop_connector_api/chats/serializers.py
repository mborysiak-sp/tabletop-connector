from rest_framework import serializers

from .models import Message, Chat


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "handle", "content", "chat")
        model = Message


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("handle", "content", "chat")
        model = Message


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "participants",
        )
        model = Chat
