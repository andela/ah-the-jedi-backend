from rest_framework_swagger.views import get_swagger_view
from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, ActivationView
)

swagger_view = get_swagger_view(title='The Jedi Authors Haven API')

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('users/activate/', ActivationView.as_view()),
]
