from .models import UserProfile
from ..follows.models import UserFollow
from ..authentication.models import User
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    """
    Handles serialization and deserialization
    of User Profile objects.
    """

    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    following = serializers.SerializerMethodField()

    bio = serializers.CharField(
        max_length=250,
        min_length=8
    )

    class Meta:
        model = UserProfile
        fields = ('first_name', "last_name", "username",
                  "email", "bio", "image",
                  "created_at", "updated_at", "following")

    def update(self, instance, validated_data):
        """Performs an update on a User Profile."""

        for (key, value) in validated_data.items():

            setattr(instance, key, value)

        instance.save()

        return instance

    def get_following(self, user):
        """
        This method 'get_following'
        defines whether the authenticated
        user follows the user associated
        with the provided username
        """

        is_following = False

        try:
            current_user = User.objects.get(
                username=self.context["request"])

            username = User.objects.get(
                username=self.context["username"])

            is_following = UserFollow.objects.filter(
                follower=current_user,
                following=username
            ).exists()

        except:
            return str(is_following)

        return str(is_following)
