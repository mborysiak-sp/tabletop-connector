from rest_framework import serializers

from .models import User, Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'firstname', 'lastname',)
        read_only_fields = ('user',)


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
