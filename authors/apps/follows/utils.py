from rest_framework.exceptions import (ParseError,
                                       NotFound, PermissionDenied)
from ..authentication.messages import errors
from ..authentication.models import User
from .models import UserFollow
from ..profiles.models import UserProfile


class Utilities:

    def get_user(self, username):
        """
        This method 'get_user' fetches
        instance of the user if it exists
        """

        return User.objects.filter(username=username).first()

    def get_followers(self, user, follower='', following=''):
        """
        This method 'get_followers' fetches all instances
        of followers to a user
        """

        try:
            return UserFollow.objects.filter(
                follower=user).exclude(following_id=follower)

        except:
            return UserFollow.objects.filter(
                following=user).exclude(follower_id=following)

    def get_profile(self, username):
        """
        This method 'get_profile' returns an instance
        of a profile if it exists
        """

        try:

            return UserProfile.objects.get(user__username=username)

        except UserProfile.DoesNotExist:

            raise NotFound(errors["profile_missing"])

    def validate_user(self, request, username):
        """
        This method 'validate_user' raises an error
        if a user tries to follow themselves
        """

        if request.user.username == username:
            raise PermissionDenied(errors["self_follow"])

    def follow_user(self, follower, followee):
        """
        This method 'follow_user' creates follow
        relationship to the specified user
        """

        try:
            follower.following.add(UserFollow(
                following=followee), bulk=False)

        except:
            raise PermissionDenied(errors["follow_exists"])

    def unfollow_user(self, follower, following):
        """
        This method 'unfollow_user' destroys follow
        relationships if exists
        """

        try:
            UserFollow.objects.get(follower=follower,
                                   following=following).delete()

        except:
            raise ParseError(errors["unfollow_failed"])
