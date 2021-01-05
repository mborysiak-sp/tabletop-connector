from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import User, Profile


class ProfileSerializer(serializers.ModelSerializer):
    avatar = SerializerMethodField()

    class Meta:
        model = Profile
        fields = ("id", "firstname", "lastname", "avatar")

    def get_avatar(self, profile):
        request = self.context.get("request")
        if profile and hasattr(profile, "avatar"):
            avatar = "/api" + profile.avatar.url
            return request.build_absolute_uri(avatar)
        else:
            return None


class CreateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("firstname", "lastname", "avatar")


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ("id", "username", "profile")
        read_only_fields = ("profile",)
        ref_name = "User serializer"


class CreateUserSerializer(WritableNestedModelSerializer):
    profile = CreateProfileSerializer(many=False)

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        profile_data = validated_data.pop("profile")
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user

    class Meta:
        model = User
        fields = ("username", "password", "profile")
        extra_kwargs = {"password": {"write_only": True}}
