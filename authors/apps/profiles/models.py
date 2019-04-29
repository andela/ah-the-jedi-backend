from django.db import models
from ..authentication.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
    """
    The User Profile Model
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    bio = models.TextField(max_length=250, blank=True)
    image = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs["instance"])


post_save.connect(create_profile, sender=User)
