import os
import datetime
import re
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import ugettext_lazy as _

from rest_framework import status, generics, permissions, views
from rest_framework.generics import (
    RetrieveUpdateAPIView, GenericAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .backends import handle_token

from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer,
    UserSerializer, UidAndTokenSerializer
)
from authors.apps.authentication.models import User
from authors.apps.core import exceptions
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist


class RegistrationAPIView(GenericAPIView):
    """
    post:
    Signup a user.
    """
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {
            "data": serializer.data,
            "message": "Account succesfully registered. Check your mail inbox to activate your account.",
        }

        return Response(data=response,
                        status=status.HTTP_201_CREATED)


class LoginAPIView(GenericAPIView):
    """
    post:
    Login a user.
    """
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        user_data = User.objects.get(email=user['email'])
        token = handle_token(user_data)
        res = serializer.data
        res['token'] = token

        return Response(res, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ActivationView(generics.GenericAPIView):
    """
    post:
    Activate user.
    """
    serializer_class = UidAndTokenSerializer
    permission_classes = [permissions.AllowAny]
    token_generator = default_token_generator

    def post(self, request):
        uid = request.GET.get("uid", "")
        token = request.GET.get("token", "")

        serializer = self.serializer_class(data={"uid": uid, "token": token})
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(id=uid)
        if user.is_active:
            raise exceptions.AlreadyProcessed(
                _('The user account is already active.'))

        user.is_active = True
        user.save()

        token = handle_token(user)

        response_data = {
            "message": "Your account has been activated.",
            "token": token
        }

        return Response(data=response_data, status=status.HTTP_200_OK)


class ResetPasswordView(GenericAPIView):
    """
    post:
    Request password reset Link.
    """
    serializer_class = UidAndTokenSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email", "")

        if not email:
            return Response({
                "error": "Email field is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        elif not re.match(r"(^[a-zA-z0-9_.]+@[a-zA-z0-9-]+\.[a-z]+$)",
                          email):
            return Response({
                "error": "Please enter a valid email address"
            }, status=status.HTTP_400_BAD_REQUEST)

        error_response = {
            "message": "Account with this email not found."
        }
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response(data=error_response,
                            status=status.HTTP_404_NOT_FOUND)

        token = default_token_generator.make_token(user)
        domain = os.getenv('DOMAIN')

        msg_html = render_to_string('reset_password.html', {"domain": domain,
                                                            'uid': user.pk,
                                                            'token': token}
                                    )

        success_response = {
            "message": "Password reset link has been sent to your email, "
            "check your email for instructions on how to change password",
            "uid": user.pk,
            "token": token
        }

        send_mail('Reset Password',
                  'Here is the message.',
                  'Authors Haven',
                  [email],
                  html_message=msg_html,
                  fail_silently=False,

                  )

        return Response(data=success_response, status=status.HTTP_200_OK)


class ResetPasswordAPIView(GenericAPIView):
    """Patch: Reset Password """
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UidAndTokenSerializer
    permission_classes = [permissions.AllowAny]

    def patch(self, request):

        uid = request.GET.get("uid", "")
        token = request.GET.get("token", "")

        password = request.data.get("password", "")

        # now we validate the password
        if not password:
            return Response({
                "error": "Password field is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        elif not re.match(r"(^[a-zA-Z0-9]{8,}$)",
                          password):
            return Response({
                "error": "A password should be only Aplhanumeric "
                "characters and a minimum of 8 characters"
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(
                data={"uid": uid, "token": token})
            serializer.is_valid(raise_exception=True)

            user = User.objects.get(id=uid)
            user.set_password(password)
            user.save()

            response_data = {
                "message":
                "Your account password has been changed successfully."
            }

            return Response(data=response_data, status=status.HTTP_200_OK)
