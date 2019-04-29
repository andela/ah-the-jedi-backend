import json
from django.http.response import Http404
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.exceptions import (ParseError, NotFound)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile
from .permissions import IsGetOrIsAuthenticated
from ..authentication.messages import errors
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer
from .utils import validate_image_upload


class ProfileRetreiveUpdateAPIView(RetrieveUpdateAPIView):
    """
    get:
    Get user profile.

    put:
    Update user profile.
    """

    permission_classes = (IsGetOrIsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def retrieve(self, request, username):
        """
        get:
        Get user profile.
        """

        try:
            user = UserProfile.objects.select_related('user').get(
                user__username=username)

        except UserProfile.DoesNotExist:

            raise NotFound(errors["profile_missing"])

        serializer = self.serializer_class(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, username):
        """
        put:
        Update user profile.

        :param username: username associated with
        user account
        :return: updated user profile details if successful
        """

        serializer_data, image = request.data, ''

        try:
            user = UserProfile.objects.select_related('user').get(
                user__username=username)

        except UserProfile.DoesNotExist:

            raise NotFound(errors["profile_missing"])

        self.check_object_permissions(request, user)

        validate_image_upload(request)

        serializer = self.serializer_class(
            user, data=serializer_data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
