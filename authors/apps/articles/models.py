from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from autoslug import AutoSlugField
from django.core.validators import URLValidator
from vote.models import VoteModel
from fluent_comments.models import FluentComment
from authors.apps.authentication.models import User


class TagModel(models.Model):
    """
    Tags for articles. The text for each tag is unique
    """

    tagname = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.tagname


class ArticleModel(VoteModel, models.Model):
    """The article model."""

    slug = AutoSlugField(populate_from='title',
                         blank=True, null=True, unique=True, always_update=True)
    title = models.CharField(max_length=254)
    description = models.TextField(blank=False, null=False)
    body = models.TextField(blank=False, null=False)
    tag_list = models.ManyToManyField(TagModel)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, editable=True)
    favorited = models.BooleanField(default=False)
    favorites_count = models.IntegerField(default=0)
    image = models.TextField(max_length=1000, validators=[
                             URLValidator], null=False, default='')
    num_vote_down = models.IntegerField(default=0)
    num_vote_up = models.IntegerField(default=0)
    vote_score = models.IntegerField(default=0)
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    mail = models.TextField(blank=False, null=False, default="")
    readtime = models.CharField(blank=False, null=False, max_length=240)

    author = models.ForeignKey(
        get_user_model(),
        related_name='article_author',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )

    def __str__(self):
        return "{}".format(self.title)  # pragma: no cover

    class Meta:
        ordering = ["-created_at"]


class FavoriteArticleModel(models.Model):
    """Favorite article model."""
    favoritor = models.ForeignKey(
        User, related_name='favorites', on_delete=models.CASCADE)

    article = models.ForeignKey(
        ArticleModel,
        related_name='favorited_article',
        on_delete=models.CASCADE)


class BookmarkArticleModel(models.Model):
    """Bookmark article model."""
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    article = models.ForeignKey(ArticleModel, blank=False, on_delete=models.CASCADE,
                                to_field='slug')
    bookmarked_at = models.DateTimeField(
        auto_created=True, auto_now=False, default=timezone.now)


class CommentHistoryModel(models.Model):
    """Comments edit history model"""
    comment = models.ForeignKey(FluentComment, on_delete=models.CASCADE)
    updated_comment = models.TextField()
    updated_at = models.DateTimeField(auto_now_add=True)


class CommentModel(VoteModel, models.Model):
    """The comment model"""
    comment = models.ForeignKey(FluentComment,
                                related_name='comment_id',
                                on_delete=models.CASCADE, default='')
    user = models.ForeignKey(
        User, related_name='user', on_delete=models.CASCADE)


class ReadStatsModel(models.Model):
    """Reading statistics model"""
    user = models.ForeignKey(
        User, related_name="read_user", on_delete=models.CASCADE)

    article = models.ForeignKey(
        ArticleModel, related_name="read_article", on_delete=models.CASCADE)
