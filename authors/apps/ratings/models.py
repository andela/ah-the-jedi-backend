"""
Ratings Models
"""
from django.db import models
from ..articles.models import ArticleModel
from ..authentication.models import User


class Ratings(models.Model):
    """
    The Ratings Model
    """
    article = models.ForeignKey(ArticleModel,
                                related_name='rated_article',
                                on_delete=models.CASCADE)

    rated_by = models.ForeignKey(User,
                                 related_name='rated_by',
                                 on_delete=models.CASCADE)

    rating = models.IntegerField(null=False)
