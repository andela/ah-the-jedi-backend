from django.db import models
from ..authentication.models import User


class UserFollow(models.Model):
    """
    The User Follower/Following Model
    """

    follower = models.ForeignKey(
        User,
        related_name="following",
        on_delete=models.CASCADE
    )

    following = models.ForeignKey(
        User,
        related_name="followers",
        on_delete=models.CASCADE
    )

    class Meta:

        unique_together = ('follower', 'following')

    def __str__(self):

        return "{} follows {}".format(
            self.follower.username,
            self.following.username
        )
