from rest_framework import serializers
from .models import Notifications, Subscriptions
from . import utils


class NotificationSerializer(serializers.ModelSerializer):
    """
    Handles serialization and deserialization
    of Notification objects
    """

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Notifications

        fields = ("url", "message", "created_at", "id", "read")

    def update(self, instance, validated_data):

        return utils.make_update(instance, validated_data)


class SubscriptionsSerializer(serializers.ModelSerializer):
    """
    Handles serialization and deserialization of
    Subscription objects
    """

    class Meta:
        model = Subscriptions

        fields = ("email", "app")

    def update(self, instance, validated_data):

        return utils.make_update(instance, validated_data)
