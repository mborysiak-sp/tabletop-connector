from rest_framework import serializers

from .models import Address, Event


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ('id', 'country', 'city', 'street', 'postal_code', 'number', )


class EventSerializer(serializers.ModelSerializer):

    address = AddressSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id', 'name', 'date', 'creator', 'address', 'chat',)

    def create(self, validated_data):

        address_data = validated_data.pop('address')
        created_address = Address.objects.create(**address_data)

        return Event.objects.create(address=created_address.pk, **validated_data)