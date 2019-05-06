"""
urls for rating an article
"""
from django.urls import path
from .views import RatingsAPIView

app_name = "ratings"

urlpatterns = [
    path("articles/<slug>/rate/", RatingsAPIView.as_view(), name='rate')

]
