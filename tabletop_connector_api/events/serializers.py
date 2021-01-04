from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from .models import Address, Event, Game
from .utils import address_to_geocode, geocode_to_address
from ..users.serializers import UserSerializer


def read_address(validated_data):
    if (
        validated_data.get("geo_x") is not None
        and validated_data.get("geo_y") is not None
    ):
        address = geocode_to_address((validated_data["geo_x"], validated_data["geo_y"]))
        try:
            validated_data["country"] = address["country"]
            validated_data["street"] = address["street"]
            validated_data["city"] = address["city"]
            validated_data["postal_code"] = address["postal_code"]
        except TypeError:
            raise serializers.ValidationError("Address not found")
    else:
        geocode = address_to_geocode(validated_data)
        if geocode == ():
            raise serializers.ValidationError("Address not found")
        try:
            validated_data["geo_x"] = geocode[0]
            validated_data["geo_y"] = geocode[1]
        except TypeError:
            raise serializers.ValidationError("Address not found")
    return validated_data


class AddressSerializer(serializers.ModelSerializer):
    geo_x = serializers.FloatField(required=False, allow_null=True)
    geo_y = serializers.FloatField(required=False, allow_null=True)

    class Meta:
        model = Address
        fields = (
            "id",
            "country",
            "city",
            "street",
            "postal_code",
            "number",
            "geo_x",
            "geo_y",
        )

    def update(self, instance, validated_data):
        validated_data = read_address(validated_data)

        instance.country = validated_data.get("country", instance.country)
        instance.city = validated_data.get("city", instance.city)
        instance.street = validated_data.get("street", instance.street)
        instance.number = validated_data.get("number", instance.number)
        instance.postal_code = validated_data.get("postal_code", instance.postal_code)
        instance.geo_x = validated_data.get("geo_x", instance.geo_x)
        instance.geo_y = validated_data.get("geo_y", instance.geo_y)
        instance.save()

        return instance


class AddressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            "country",
            "city",
            "street",
            "postal_code",
            "number",
            "geo_x",
            "geo_y",
        )

    def create(self, validated_data):
        validated_data = read_address(validated_data)
        return Address.objects.create(**validated_data)


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = "__all__"


class EventCreateSerializer(WritableNestedModelSerializer):
    address = AddressCreateSerializer(many=False)
    participants = UserSerializer(many=True, read_only=True)
    creator = UserSerializer(many=False, read_only=True)
    games = GameSerializer(many=True, read_only=False, default=[])

    class Meta:
        model = Event
        read_only_fields = (
            "id",
            "creator",
            "participants",
            "chat",
            # "games",
        )
        fields = (
            "id",
            "name",
            "date",
            "address",
            "participants",
            "creator",
            "chat",
            "games",
        )


class EventSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=False)
    participants = UserSerializer(many=True)
    creator = UserSerializer(many=False)
    games = GameSerializer(many=True)

    class Meta:
        model = Event
        fields = (
            "id",
            "name",
            "date",
            "creator",
            "address",
            "chat",
            "participants",
            "games",
        )
