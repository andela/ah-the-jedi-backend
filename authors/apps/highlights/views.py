from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status

from ..articles.models import ArticleModel
from .serializers import HighlightsSerializer
from .models import HighlightsModel


class HighlightArticleView(GenericAPIView):
    """Highlight an article view"""
    permission_classes = [IsAuthenticated]
    serializer_class = HighlightsSerializer

    def post(self, request, *args, **kwargs):
        """Highlight an article"""

        slug = self.kwargs.get('slug')
        article = ArticleModel.objects.all().filter(slug=slug).first()
        user = request.user
        highlight = request.data.get("highlight", "")
        location = request.data["location"]

        if article is None:
            response = {
                'error': 'Article with slug {} not found'.format(slug)
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)
        if location == "description":
            expected_text = article.description
        elif location == "title":
            expected_text = article.title
        elif location == "body":
            expected_text = article.body

        if highlight not in expected_text:
            return Response({
                "error": "The highlighted text is not found in this article {}".format(location),
                "status": 404
            }, status=404)

        existing_highlight = HighlightsModel.objects.all().filter(
            article=article.id, highlighted_by=user.id, highlight=highlight.lstrip(), location=location, position=expected_text.find(highlight))
        if existing_highlight:
            return Response({
                "error": "You have already highlighted this article",
                "status": 409
            }, status=409)

        request.data['position'] = expected_text.find(highlight)
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(article=article, highlighted_by=user)

        return Response({
            "data": serializer.data
        })
