from rest_framework import serializers
from .models import HighlightsModel


class HighlightsSerializer(serializers.ModelSerializer):

    """
    Handles serialization and deserialization
    of Highlights objects
    """
    article = serializers.SerializerMethodField(
        method_name='highlighted_article')
    highlighted_by = serializers.SerializerMethodField(
        method_name='highlighter')
    comment = serializers.CharField()
    highlight = serializers.CharField()

    class Meta:
        model = HighlightsModel
        fields = ('article',
                  'highlighted_by',
                  'comment',
                  'highlight',
                  'location',)

    def highlighted_article(self, instance):
        """
        Get the slug of the article that is being highlighted
        """
        return instance.article.slug

    def highlighter(self, instance):
        """
        Get the username of the person highlighting the article
        """
        return instance.highlighted_by.username
