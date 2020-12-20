from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import User, Profile


class ProfileSerializer(serializers.ModelSerializer):
    image = SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('id', 'firstname', 'lastname', 'image')

    def get_image(self, profile):
        request = self.context.get('request')
        if profile and hasattr(profile, 'image'):
            image = profile.image.url
            return request.build_absolute_uri(image)
        else:
            return None


class CreateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('firstname', 'lastname', 'avatar')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'profile')
        read_only_fields = ('profile',)


class CreateUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'email',)
        extra_kwargs = {'password': {'write_only': True}}
