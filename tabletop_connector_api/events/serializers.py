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
        fields = ('id', 'name', 'date', 'creator', 'address', 'chat', 'participants',)

    def create(self, validated_data):

        address_data = validated_data.pop('address')
        geocode = address_to_geocode(address_data)
        if geocode == ():
            return None
        address_data['geo_x'] = geocode[0]
        address_data['geo_y'] = geocode[1]
        created_address = Address.objects.create(**address_data)
        return Event.objects.create(address=created_address, **validated_data)

    def update(self, instance, validated_data):

        address_data = validated_data.get('address', instance.address)
        geocode = address_to_geocode(address_data)
        if geocode == ():
            return None
        address_data['geo_x'] = geocode[0]
        address_data['geo_y'] = geocode[1]
        # created_address = Address.objects.create(**address_data) 1)   if want to override address
        # instance.address = created_address                            this too
        instance.address.country = address_data.get('country', instance.address.country)
        instance.address.city = address_data.get('city', instance.address.city)
        instance.address.street = address_data.get('street', instance.address.street)
        instance.address.number = address_data.get('number', instance.address.number)
        instance.address.postal_code = address_data.get('postal_code', instance.address.postal_code)
        instance.address.geo_x = address_data.get('geo_x', instance.address.geo_x)
        instance.address.geo_y = address_data.get('geo_y', instance.address.geo_y)
        instance.address.save()
        instance.name = validated_data.get('name', instance.name)
        instance.date = validated_data.get('date', instance.date)
        instance.participants = validated_data.get('participants', instance.participants)

        instance.save()
        return instance
