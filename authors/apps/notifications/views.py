from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.generics import (
    RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView)
from rest_framework.permissions import IsAuthenticated

from . import utils
from .serializers import NotificationSerializer, SubscriptionsSerializer
from ..authentication.messages import errors


def retreive_notifications(username, request, read=None):
    """
    This method retreive notifications
    fetches read, unread and all
    notifications based on the parameters
    provided
    """

    paginator = utils.PageNumberPaginationNotifications()

    paginator.page_size = request.GET.get('limit', '9')

    user = utils.get_user(username)

    notifications = utils.get_notification(user, read=read)

    count = notifications.count()

    page = paginator.paginate_queryset(notifications, request)

    serializer = NotificationSerializer(page, many=True)

    response = paginator.get_paginated_response(data=serializer.data)

    return response if count else Response(
        {"notifications": "You do not have any notifications"})


class NotificationRetreiveView(RetrieveAPIView):
    """
    get:
    Get all user notifications
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    def retrieve(self, request):
        """
        get:
        Fetch all user notifications
        """

        return retreive_notifications(request.user.username, request, None)


class ReadRetreiveView(RetrieveAPIView):
    """
    get:
    Get all read user notifications
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    def retrieve(self, request):
        """
        get:
        Fetch all read user notifications
        """

        return retreive_notifications(request.user.username, request, True)


class UnreadRetreiveView(RetrieveAPIView):
    """
    get:
    Get all unread user notifications
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    def retrieve(self, request):
        """
        get:
        Fetch all unread user notifications
        """

        return retreive_notifications(request.user.username, request, False)


class ReadUpdateView(UpdateAPIView):
    """
    put:
    read user notification
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    def update(self, request, pk):
        """
        put:
        read user notification
        """

        serializer_data = {"read": "True"}

        notifications = utils.get_notification(user=pk, single=True)

        if not notifications:
            raise NotFound(errors["notification_missing"])

        utils.check_is_object_owner(notifications, request)

        serializer = self.serializer_class(
            notifications, data=serializer_data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        response = {"notification": serializer.data}

        return Response(response, status=status.HTTP_200_OK)


class SubscriptionUpdateView(RetrieveUpdateAPIView):
    """
    get:
    Get user subscriptions

    put:
    Update user subscriptions
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = SubscriptionsSerializer

    def retrieve(self, request):
        """
        get:
        Fetch user subscriptions
        """

        user = utils.get_subscriptions(request.user)

        serializer = self.serializer_class(user)

        response = {"subscriptions": serializer.data}

        return Response(response, status=status.HTTP_200_OK)

    def update(self, request):
        """
        put:
        Update user subscriptions
        """

        serializer_data = request.data

        user = utils.get_subscriptions(request.user)

        serializer = self.serializer_class(
            user, data=serializer_data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        response = {"subscriptions": serializer.data}

        return Response(response, status=status.HTTP_200_OK)
