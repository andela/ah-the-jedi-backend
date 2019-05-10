from django.urls import path
from .views import (NotificationRetreiveView,
                    ReadRetreiveView, ReadUpdateView, UnreadRetreiveView,
                    SubscriptionUpdateView)


urlpatterns = [
    path('notifications/all', NotificationRetreiveView.as_view(),
         name="user_notifications"),
    path('notifications/subscriptions', SubscriptionUpdateView.as_view(),
         name="user_subscriptions"),
    path('notifications/read', ReadRetreiveView.as_view(),
         name="notifications_read"),
    path('notifications/read/<pk>', ReadUpdateView.as_view(),
         name="user_read"),
    path('notifications/unread', UnreadRetreiveView.as_view(),
         name="notifications_unread"),
]
