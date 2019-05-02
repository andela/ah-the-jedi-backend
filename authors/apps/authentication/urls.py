from rest_framework_swagger.views import get_swagger_view
from django.urls import path
from django.conf.urls import url

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    ActivationView, ResetPasswordView, ResetPasswordAPIView, SocialLoginView
)

swagger_view = get_swagger_view(title='The Jedi Authors Haven API')

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('users/activate/', ActivationView.as_view()),
    path('users/reset_password/', ResetPasswordView.as_view()),
    path('users/reset_password_confirm/', ResetPasswordAPIView.as_view()),
    url(r'^$', swagger_view),
    path('users/social/login/', SocialLoginView.as_view())
]
