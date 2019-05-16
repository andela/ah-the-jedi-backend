from django.db.models.signals import post_save
from fluent_comments.models import FluentComment

from ..articles import models
from ..authentication.models import User
from ..follows.models import UserFollow
from .utils import (create_comment_notification,
                    create_post_notification, create_subscriptions,
                    create_follow_notification)


post_save.connect(create_subscriptions, sender=User)

post_save.connect(create_follow_notification, sender=UserFollow)

post_save.connect(create_post_notification, sender=models.ArticleModel)

post_save.connect(create_comment_notification, sender=FluentComment)
