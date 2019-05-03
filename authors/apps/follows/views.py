from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import (
    RetrieveAPIView, CreateAPIView, DestroyAPIView)
from rest_framework.response import Response

from .models import UserFollow
from .utils import Utilities
from .serializers import FollowsSerializer, FollowersSerializer
from ..profiles.permissions import IsGetOrIsAuthenticated
from ..profiles.renderers import ProfileJSONRenderer
from ..profiles.serializers import ProfileSerializer


class UserFollowingRetrieveView(RetrieveAPIView):
    """
    get:
    Get users that the user follows.
    """

    permission_classes = (IsGetOrIsAuthenticated,)
    serializer_class = FollowsSerializer

    def retrieve(self, request):
        """
        get:
        Get profile that user follows
        """

        user = Utilities.get_user(self, request.user.username)

        following = Utilities.get_followers(
            self, user=user, follower=request.user.id)

        context = {"user": user}

        serializer = self.serializer_class(
            following, many=True, context=context)

        response = {
            "users": serializer.data,
            "following": user.following.all().count()
        }

        return Response({"data": response},
                        status=status.HTTP_200_OK)


class UserFollowersRetrieveView(RetrieveAPIView):
    """
    get:
    Get users that follow the user's profile.
    """

    permission_classes = (IsGetOrIsAuthenticated,)
    serializer_class = FollowersSerializer

    def retrieve(self, request):
        """
        get:
        Get users follow the user's profile
        """

        user = Utilities.get_user(self, request.user.username)

        follower = Utilities.get_followers(
            self, user=user, following=request.user.id)

        context = {"user": user}

        serializer = self.serializer_class(
            follower, many=True, context=context)

        response = {
            "users": serializer.data,
            "followers": user.followers.all().count()
        }

        return Response({"data": response},
                        status=status.HTTP_200_OK)


class FollowUserView(CreateAPIView):

    permission_classes = (IsGetOrIsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def post(self, request, username):
        """
        post:
        Follow users
        """

        user = Utilities.get_profile(self, username)

        current_user = Utilities.get_user(self, username)

        request_user = Utilities.get_user(self, request.user.username)

        Utilities.validate_user(self, request, username)

        context = {
            "request": request.user.username,
            "username": username
        }

        Utilities.follow_user(self, follower=request_user,
                              followee=current_user)

        serializer = self.serializer_class(user, context=context)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UnfollowUserView(DestroyAPIView):
    """
    delete:
    Unfollow users
    """

    permission_classes = (IsGetOrIsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def delete(self, request, username):
        """
        delete:
        Unfollow users
        """

        user = Utilities.get_profile(self, username)

        current_user = Utilities.get_user(self, username)

        request_user = Utilities.get_user(self, request.user.username)

        context = {
            "request": request.user.username,
            "username": username
        }

        Utilities.unfollow_user(
            self, follower=request_user, following=current_user)

        serializer = self.serializer_class(user, context=context)

        return Response(serializer.data, status=status.HTTP_200_OK)
