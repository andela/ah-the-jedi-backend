from django.urls import path
from .views import (UserFollowingRetrieveView,
                    UserFollowersRetrieveView, FollowUserView,
                    UnfollowUserView)


urlpatterns = [
    path('user/following', UserFollowingRetrieveView.as_view(),
         name="user_following"),
    path('user/followers', UserFollowersRetrieveView.as_view(),
         name="user_followers"),
    path('profiles/<username>/follow', FollowUserView.as_view(),
         name="user_follow"),
    path('profiles/<username>/unfollow', UnfollowUserView.as_view(),
         name="user_unfollow"),
]
