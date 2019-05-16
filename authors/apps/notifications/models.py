from django.db import models

from ..authentication.models import User
from . import utils, actions


class Notifications(models.Model):
    """
    The Notifications Model
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE)

    message = models.CharField(max_length=200)

    url = models.CharField(max_length=200)

    read = models.BooleanField(default=False)

    createdAt = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ["-createdAt"]

    def __str__(self):

        return self.message  # pragma: no cover


class Subscriptions(models.Model):
    """
    The Subscriptions model
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE)

    email = models.BooleanField(default=True)

    app = models.BooleanField(default=True)
