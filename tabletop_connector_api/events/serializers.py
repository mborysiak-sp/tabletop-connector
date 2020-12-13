from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from .models import Address, Event
from .utils import address_to_geocode


class AddressSerializer(serializers.ModelSerializer):
    geo_x = serializers.FloatField(required=False, allow_null=True)
    geo_y = serializers.FloatField(required=False, allow_null=True)

    class Meta:
        model = Address
        fields = ('id', 'country', 'city', 'street', 'postal_code', 'number', 'geo_x', 'geo_y',)

    def update(self, instance, validated_data):
        geocode = address_to_geocode(validated_data)
        if geocode == ():
            return None

        instance.country = validated_data.get('country', instance.country)
        instance.city = validated_data.get('city', instance.city)
        instance.street = validated_data.get('street', instance.street)
        instance.number = validated_data.get('number', instance.number)
        instance.postal_code = validated_data.get('postal_code', instance.postal_code)
        instance.geo_x = geocode[0]
        instance.geo_y = geocode[1]
        instance.save()

        return instance


class AddressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('country', 'city', 'street', 'postal_code', 'number',)

    def create(self, validated_data):
        geocode = address_to_geocode(validated_data)
        if geocode == ():
            return None
        validated_data['geo_x'] = geocode[0]
        validated_data['geo_y'] = geocode[1]
        return Address.objects.create(**validated_data)


class EventCreateSerializer(WritableNestedModelSerializer):
    address = AddressCreateSerializer(many=False)

    class Meta:
        model = Event
        fields = ('name', 'date', 'address',)

    read_only_fields = ('creator', 'participants')


class EventSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id', 'name', 'date', 'creator', 'address', 'chat', 'participants',)

    # def update(self, instance, validated_data):
    #
    #     address_data = validated_data.get('address', instance.address)
    #     geocode = address_to_geocode(address_data)
    #     if geocode == ():
    #         return None
    #     address_data['geo_x'] = geocode[0]
    #     address_data['geo_y'] = geocode[1]
    #     # created_address = Address.objects.create(**address_data) 1)   if want to override address
    #     # instance.address = created_address                            this too
    #     instance.address.country = address_data.get('country', instance.address.country)
    #     instance.address.city = address_data.get('city', instance.address.city)
    #     instance.address.street = address_data.get('street', instance.address.street)
    #     instance.address.number = address_data.get('number', instance.address.number)
    #     instance.address.postal_code = address_data.get('postal_code', instance.address.postal_code)
    #     instance.address.geo_x = address_data.get('geo_x', instance.address.geo_x)
    #     instance.address.geo_y = address_data.get('geo_y', instance.address.geo_y)
    #     instance.address.save()
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.date = validated_data.get('date', instance.date)
    #     instance.participants = validated_data.get('participants', instance.participants)
    #     instance.save()
    #
    #     return instance
