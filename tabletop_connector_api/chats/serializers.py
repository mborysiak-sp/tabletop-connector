from rest_framework import serializers

from .models import Message, Chat


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "handle", "content", "timestamp")
        model = Message


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("handle", "content", "chat")
        model = Message


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True)

    class Meta:
        fields = (
            "id",
            "participants",
            "messages"
        )
        model = Chat
