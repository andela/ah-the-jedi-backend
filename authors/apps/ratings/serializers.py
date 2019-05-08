"""
Ratings serializers
"""
from rest_framework import serializers
from .models import Ratings
from django.db.models import Avg


class RatingsSerializer(serializers.ModelSerializer):

    """
    Handles serialization and deserialization
    of Ratings objects
    """
    article = serializers.SerializerMethodField(method_name='rated_article')
    rated_by = serializers.SerializerMethodField(method_name='rater')
    rating = serializers.IntegerField(min_value=0, max_value=5, required=True)
    author = serializers.SerializerMethodField(method_name='article_author')
    averate_article_rating = serializers.SerializerMethodField(
        method_name="average_rating"
    )

    class Meta:
        model = Ratings
        fields = ('article',
                  'rated_by',
                  'author',
                  'rating',
                  'averate_article_rating')

    def rated_article(self, instance):
        """
        Get the slug of the article that is being rated
        """
        return instance.article.slug

    def rater(self, instance):
        """
        Get the username of the person rating the article
        """
        return instance.rated_by.username

    def article_author(self, instance):
        """
        Get the author of the article that is being rated
        """
        return instance.article.author.username

    def average_rating(self, instance):
        """
        Get the average rating of an article
        """
        average_rate = Ratings.objects.filter(article=instance.article,
                                              ).aggregate(rate=Avg('rating'))

        if average_rate["rate"]:
            return float('%.2f' % (average_rate["rate"]))
        return 0
