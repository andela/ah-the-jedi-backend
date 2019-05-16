from django.db import models

from authors.apps.articles.models import ArticleModel
from django.contrib.auth import get_user_model


class ReportModel(models.Model):
    """
    The report model
    """

    user = models.ForeignKey(
        get_user_model(),
        related_name='reporter',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )

    article = models.ForeignKey(
        ArticleModel,
        related_name='reported',
        on_delete=models.CASCADE
    )

    reason = models.TextField(max_length=700)
    createdAt = models.DateTimeField(auto_now_add=True, editable=False)
    updatedAt = models.DateTimeField(auto_now_add=True, editable=True)

    def __str__(self):
        return "{}".format(self.user.username)  # pragma: no cover

    class Meta:
        ordering = ["-createdAt"]
