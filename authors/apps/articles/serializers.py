from rest_framework import serializers
from django.apps import apps
from .models import ArticleModel, FavoriteArticleModel, BookmarkArticleModel
from fluent_comments.models import FluentComment
from .utils import user_object, configure_response
from django.contrib.auth.models import AnonymousUser
from django.db.models import Avg
from authors.apps.ratings.models import Ratings
from ..highlights.models import HighlightsModel
from ..highlights.serializers import HighlightsSerializer


TABLE = apps.get_model('articles', 'ArticleModel')


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(
            value,
            context=self.context)  # pragma: no cover
        return serializer.data  # pragma: no cover


class CommentSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)

    class Meta:
        model = FluentComment

        fields = (
            'id',
            'comment',
            'children',
            'submit_date',
            'user_id')


class ArticleSerializer(serializers.ModelSerializer):
    """The article serializer."""
    comments = serializers.SerializerMethodField()
    favorited = serializers.SerializerMethodField()
    favoritesCount = serializers.SerializerMethodField()
    highlights = serializers.SerializerMethodField()

    average_rating = serializers.SerializerMethodField(
        method_name='rating',
        read_only=True)

    class Meta:
        model = TABLE
        fields = (
            'id',
            'url',
            'slug',
            'title',
            'description',
            'body',
            'tagList',
            'createdAt',
            'updatedAt',
            'favorited',
            'favoritesCount',
            'average_rating',
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
        )
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}

    def create(self, validated_data):
        article = TABLE.objects.create(**validated_data)
        return article

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
        request = self.context.get('request')
        if request.user.is_anonymous:
            return True
        if request:
            return False

    def get_favoritesCount(self, obj):

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

    def get_highlights(self, obj):

        if self.check_anonymous():
            return None

        highlighted = HighlightsModel.objects.filter(
            article=obj,
            highlighted_by=self.context['request'].user)

        if highlighted:
            serializer = HighlightsSerializer(highlighted, many=True)
            return serializer.data

        return None


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
