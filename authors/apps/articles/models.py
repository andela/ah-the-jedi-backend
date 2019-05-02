from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from authors.apps.authentication.models import User
from autoslug import AutoSlugField
from django.core.validators import URLValidator
from django.template.defaultfilters import slugify


class ArticleModel(models.Model):
    """The article model."""

    slug = AutoSlugField(populate_from='title',
                         blank=True, null=True, unique=True, always_update=True)
    title = models.CharField(max_length=254)
    description = models.TextField(blank=False, null=False)
    body = models.TextField(blank=False, null=False)
    tagList = ArrayField(models.TextField(
        max_length=128), blank=True, default=list)
    createdAt = models.DateTimeField(auto_now_add=True, editable=False)
    updatedAt = models.DateTimeField(auto_now_add=True, editable=True)
    favorited = models.BooleanField(default=False)
    favoritesCount = models.IntegerField(default=0)
    image = models.TextField(max_length=1000, validators=[
                             URLValidator], null=False, default='')

    author = models.ForeignKey(
        get_user_model(),
        related_name='article_author',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )

    # author = models.ForeignKey('auth.User', related_name='author', on_delete=models.CASCADE,)

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        ordering = ["-createdAt"]
