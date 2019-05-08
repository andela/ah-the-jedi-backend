"""
Ratings Views
"""
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status

from .models import Ratings, ArticleModel
from .serializers import RatingsSerializer


class RatingsAPIView(GenericAPIView):
    """
    get:
    Get article ratings.

    post:
    rate and article.
    """

    queryset = Ratings.objects.all()
    serializer_class = RatingsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_article_if_exists(self, slug):
        """
        Method to check whether the article being referenced exists in the db
        """
        article = ArticleModel.objects.all().filter(slug=slug).first()

        if not article:
            raise ValidationError(
                detail={"message": "article not found"}
            )

        return article

    def post(self, request, slug):
        """[Post a rating on an article]

        Arguments:
            request {[dictionary]} -- [the rating data]
            slug {[string]} -- [the slug of the article]
        """

        rate = request.data
        article = self.get_article_if_exists(slug)

        if request.user == article.author:
            raise ValidationError(
                detail={"message": "You cannot rate your own article"}
            )

        # check if user have rated article and update it if true
        try:
            existing_rating = Ratings.objects.get(article=article,
                                                  rated_by=request.user)

            serializer = self.serializer_class(existing_rating, data=rate)
        except Ratings.DoesNotExist:
            serializer = self.serializer_class(data=rate)

        serializer.is_valid(raise_exception=True)
        serializer.save(article=article, rated_by=request.user)

        return Response({
            'message': 'Article rating successful',
            'Rating': serializer.data
        }, status=status.HTTP_201_CREATED)
