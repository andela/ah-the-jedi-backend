from django.urls import path

from .views import (
    ProfileRetreiveUpdateAPIView
)

urlpatterns = [
    path("profiles/<username>",
         ProfileRetreiveUpdateAPIView.as_view()),
]
