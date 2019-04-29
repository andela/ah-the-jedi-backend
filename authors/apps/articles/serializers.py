from rest_framework import serializers
from django.apps import apps
from .models import ArticleModel

TABLE = apps.get_model('articles', 'ArticleModel')


class ArticleSerializer(serializers.ModelSerializer):
    """The article serializer."""

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
            'image'
        )
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}

    def create(self, validated_data):
        article = TABLE.objects.create(**validated_data)
        return article
