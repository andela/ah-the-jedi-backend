from django.db import models
from ..articles.models import ArticleModel
from ..authentication.models import User


class HighlightsModel(models.Model):
    """
    The Highlight articles Model
    """
    article = models.ForeignKey(ArticleModel,
                                related_name='article',
                                on_delete=models.CASCADE)

    highlighted_by = models.ForeignKey(User,
                                       related_name='highlighted_by',
                                       on_delete=models.CASCADE)

    highlight = models.TextField(blank=False, null=False)
    comment = models.TextField(blank=False, null=False)
    location = models.TextField(blank=False, null=False)
    position = models.IntegerField(blank=False, null=False)
