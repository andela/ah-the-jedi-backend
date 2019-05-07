from django.urls import path

from .views import (
    ProfileRetreiveUpdateAPIView, ListProfilesView
)

urlpatterns = [
    path("profiles/<username>",
         ProfileRetreiveUpdateAPIView.as_view()),
    path("profiles/", ListProfilesView.as_view())
]
