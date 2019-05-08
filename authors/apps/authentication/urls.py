from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    ActivationView, ResetPasswordView, ResetPasswordAPIView, SocialLoginView
)


urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('users/activate/', ActivationView.as_view()),
    path('users/reset_password/', ResetPasswordView.as_view()),
    path('users/reset_password_confirm/', ResetPasswordAPIView.as_view()),
    path('users/social/login/', SocialLoginView.as_view())
]
