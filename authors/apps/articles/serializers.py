from rest_framework import serializers
from django.apps import apps
from .models import (ArticleModel, FavoriteArticleModel,
                     BookmarkArticleModel, TagModel,
                     CommentHistoryModel, CommentModel, ReadStatsModel)
from fluent_comments.models import FluentComment
from .utils import user_object, configure_response, TagField
from django.contrib.auth.models import AnonymousUser
from django.db.models import Avg
from authors.apps.ratings.models import Ratings
from ..highlights.models import HighlightsModel
from ..highlights.serializers import HighlightsSerializer

from rest_framework.response import Response

TABLE = apps.get_model('articles', 'ArticleModel')


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(
            value,
            context=self.context)  # pragma: no cover

        response = serializer.data     # pragma: no cover
        response['author'] = user_object(
            response['user_id'])    # pragma: no cover

        comment_votes = CommentModel.objects.filter(
            comment=response['id']).first()

        response['votes'] = comment_votes.vote_score   # pragma: no cover
        response['num_vote_down'] = comment_votes.num_vote_down     # pragma: no cover
        response['num_vote_up'] = comment_votes.num_vote_up      # pragma: no cover
        del response['user_id']   # pragma: no cover

        return response


class CommentSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True, required=False)

    class Meta:
        model = FluentComment

        fields = (
            'id',
            'comment',
            'children',
            'submit_date',
            'user_id',)


class ArticleSerializer(serializers.ModelSerializer):
    """The article serializer."""
    comments = serializers.SerializerMethodField()
    favorited = serializers.SerializerMethodField()
    favorites_count = serializers.SerializerMethodField()
    highlights = serializers.SerializerMethodField()

    average_rating = serializers.SerializerMethodField(
        method_name='rating',
        read_only=True)

    user_rating = serializers.SerializerMethodField()

    tag_list = TagField(
        many=True,
        required=False
    )
    read_count = serializers.SerializerMethodField()
    article_readers = serializers.SerializerMethodField()

    class Meta:
        model = TABLE
        fields = (
            'id',
            'url',
            'slug',
            'title',
            'description',
            'body',
            'tag_list',
            'created_at',
            'updated_at',
            'favorited',
            'favorites_count',
            'average_rating',
            'user_rating',
            'author',
            'image',
            'comments',
            'num_vote_down',
            'num_vote_up',
            'vote_score',
            'twitter',
            'facebook',
            'mail',
            'readtime',
            'highlights',
            'read_count',
            'article_readers',
            'is_liked',
        )
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}

    def get_comments(self, obj):
        comment = FluentComment.objects.filter(
            object_pk=obj.slug, parent_id=None)
        serializer = CommentSerializer(comment, many=True)

        data = configure_response(serializer)

        return data

    def get_favorited(self, obj):

        if self.check_anonymous():
            return False

        favorited = FavoriteArticleModel.objects.filter(
            article=obj,
            favoritor=self.context['request'].user)

        if favorited:
            return True
        return False

    def check_anonymous(self):
        """
        Check if the current user is authenticated
        """
        request = self.context.get('request')
        if request.user.is_anonymous:
            return True
        return False

    def get_favorites_count(self, obj):

        favorited_articles = FavoriteArticleModel.objects.all().filter(
            article=obj).count()
        return favorited_articles

    def rating(self, obj):
        """
        Get the average rating of an article
        """
        average_rate = Ratings.objects.filter(article=obj,
                                              ).aggregate(rate=Avg('rating'))

        if average_rate["rate"]:
            return float('%.2f' % (average_rate["rate"]))
        return 0

    def get_user_rating(self, obj):
        """
        Get the rating of the logged in user
        """
        if not self.check_anonymous():
            request = self.context.get('request')
            rating = Ratings.objects.filter(
                article=obj, rated_by=request.user).first()
            if rating:
                return rating.rating

    def get_highlights(self, obj):

        if self.check_anonymous():
            return None

        highlighted = HighlightsModel.objects.filter(
            article=obj,
            highlighted_by=self.context['request'].user)

        if highlighted:
            serializer = HighlightsSerializer(
                highlighted, many=True)    # pragma: no cover
            return serializer.data

        return None

    def get_read_count(self, obj):
        """
        Return the number of people who have read an article
        This is visible to all logged in users
        """
        if not self.check_anonymous():
            read = ReadStatsModel.objects.filter(article=obj).count()

            if read:
                return read
            return 0
        return None

    def get_article_readers(self, obj):
        """
        Get the usernames of people who have read an article
        This is only visible to the author of the article
        """
        if self.check_anonymous():
            return None

        request = self.context.get('request')

        if request.user != obj.author:
            return None

        read = ReadStatsModel.objects.filter(article=obj)
        users = [x.user.username for x in read]

        return users


class FavoriteArticleSerializer(serializers.ModelSerializer):
    """Favorite article serializer"""

    article = serializers.SerializerMethodField(method_name='is_article')
    favorited = serializers.SerializerMethodField(method_name='is_favorited')

    class Meta:
        model = FavoriteArticleModel
        fields = (
            'article',
            'favorited'
        )

    def is_favorited(self, obj):
        queryset = FavoriteArticleModel.objects.filter(
            favoritor=obj.favoritor, article=obj.article)

        if queryset:
            return True
        return False

    def is_article(self, obj):
        return obj.article.slug


class BookmarkArticleSerializer(serializers.ModelSerializer):
    """Bookmark article serializer."""

    author = serializers.ReadOnlyField(source='article.author.username')
    slug = serializers.ReadOnlyField(source='article.slug')
    image = serializers.ReadOnlyField(source='article.image')
    title = serializers.ReadOnlyField(source='article.title')
    description = serializers.ReadOnlyField(source='article.description')

    class Meta:
        model = BookmarkArticleModel
        fields = ['author', 'title', 'slug',
                  'description', 'bookmarked_at', 'image']


class TagSerializer(serializers.ModelSerializer):
    """Tag an article serializer"""

    class Meta:
        model = TagModel
        fields = ('tagname',)

    def to_representation(self, instance):
        return instance.tagname


class CommentHistorySerializer(serializers.ModelSerializer):
    """Comment edit history serializer"""

    class Meta:
        model = CommentHistoryModel
        fields = ['updated_comment', 'updated_at']
