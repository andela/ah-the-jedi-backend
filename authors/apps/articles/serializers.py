from rest_framework import serializers
from django.apps import apps
from .models import ArticleModel, FavoriteArticleModel
from fluent_comments.models import FluentComment
from .utils import user_object, configure_response

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
            'author',
            'image',
            'comments',
            'num_vote_down',
            'num_vote_up',
            'vote_score',
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
        favorited = FavoriteArticleModel.objects.filter(
            article=obj,
            favoritor=self.context['request'].user)

        # import pdb
        # pdb.set_trace()

        if favorited:
            return True
        return False


class FavoriteArticleSerializer(serializers.ModelSerializer):
    """Favorite article serializer"""

    article = serializers.SerializerMethodField(method_name='is_article')
    favorited = serializers.SerializerMethodField(method_name='is_favorited')
    favoritor = serializers.SerializerMethodField(method_name='is_favoritor')

    class Meta:
        model = FavoriteArticleModel
        fields = (
            'article',
            'favoritor',
            'favorited',
        )

    def is_favorited(self, obj):
        queryset = FavoriteArticleModel.objects.filter(
            favoritor=obj.favoritor, article=obj.article)

        if queryset:
            return True
        return False

    def is_article(self, obj):
        return obj.article.slug

    def is_favoritor(self, obj):
        return obj.favoritor.username
