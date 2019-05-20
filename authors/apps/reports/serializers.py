from rest_framework import serializers
from .models import ReportModel
from django.apps import apps

TABLE = apps.get_model('reports', 'ReportModel')


class ReportSerializer(serializers.ModelSerializer):
    """
    The report serializer.
    """

    reporter = serializers.SerializerMethodField()
    reported_article = serializers.SerializerMethodField()

    class Meta:
        model = ReportModel
        fields = (
            'id',
            'user',
            'article',
            'reporter',
            'reported_article',
            'reason',
            'created_at',
            'updated_at'
        )

        extra_kwargs = {
            'reason': {'required': True},
            'user': {'write_only': True},
            'article': {'write_only': True}
        }

    def get_reporter(self, obj):
        return {
            "id": obj.user.id,
            "username": obj.user.username,
            "email": obj.user.email,
        }

    def get_reported_article(self, obj):
        return {
            "id": obj.article.id,
            "slug": obj.article.slug,
            "title": obj.article.title,
            "description": obj.article.description,
            "author": obj.article.author
        }
