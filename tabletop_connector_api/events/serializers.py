from rest_framework import serializers

from .models import Address, Event
from .utils import address_to_geocode


class AddressSerializer(serializers.ModelSerializer):

    geo_x = serializers.FloatField(required=False, allow_null=True)
    geo_y = serializers.FloatField(required=False, allow_null=True)

    class Meta:
        model = Address
        fields = ('id', 'country', 'city', 'street', 'postal_code', 'number', 'geo_x', 'geo_y', )



class EventSerializer(serializers.ModelSerializer):

    address = AddressSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id', 'name', 'date', 'creator', 'address', 'chat',)

    def create(self, validated_data):

        address_data = validated_data.pop('address')
        geocode = address_to_geocode(address_data)
        if geocode == ():
            return None
        address_data['geo_x'] = geocode[0]
        address_data['geo_y'] = geocode[1]
        created_address = Address.objects.create(**address_data)
        return Event.objects.create(address=created_address, **validated_data)
