# from ..profiles.models import UserProfile
from .models import UserFollow
from rest_framework import serializers


class FollowsSerializer(serializers.ModelSerializer):
    """
    Handles serialization and deserialization
    of User Following objects.
    """
    class Meta:
        model = UserFollow
        fields = '__all__'

    def to_representation(self, obj):

        return {
            "username": obj.following.username
        }


class FollowersSerializer(serializers.ModelSerializer):
    """
    Handles serialization and deserialization
    of User Followers objects.
    """

    class Meta:
        model = UserFollow
        fields = '__all__'

    def to_representation(self, obj):

        return {
            "username": obj.follower.username
        }
