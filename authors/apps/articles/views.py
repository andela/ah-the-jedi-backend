"""
Article Views
"""
import readtime
from rest_framework import filters, status, viewsets
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User
from ..authentication.models import User
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser, AllowAny
)
from django.utils import timezone
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from fluent_comments.models import FluentComment
from .serializers import (ArticleSerializer,
                          CommentSerializer, FavoriteArticleSerializer,
                          BookmarkArticleSerializer, TagSerializer,
                          CommentHistorySerializer)
from .models import (ArticleModel, FavoriteArticleModel,
                     BookmarkArticleModel, TagModel, CommentHistoryModel, CommentModel)
from .utils import (ImageUploader, user_object,
                    configure_response, add_social_share, ArticleFilter,
                    get_comment_queryset, check_article)
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django_comments import get_model as get_comments_model


class ArticleView(viewsets.ModelViewSet):
    """
    The article View
    """

    queryset = ArticleModel.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'slug'

    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'update': [IsAuthenticated],
        'destroy': [IsAuthenticated],
    }

    def get_permissions(self):
        """
        Function to handle permissions
        """
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:  # pragma: no cover
            return [permission() for permission in self.permission_classes]  # pragma: no cover

    def create(self, request):
        """
        post:
        The create article endpoint
        """
        userid = request.user.id
        title = request.data.get('title')
        body = request.data.get('body')

        if self.check_if_duplicate(userid, title, body):
            return JsonResponse(
                {"status": 409,
                 "error": "Article exists"},
                status=409)

        request.POST._mutable = True
        file_exists = request.FILES.get('image', False)

        if file_exists:
            return self.upload_image(request)
        if not file_exists:
            return self.create_article(request)

    def list(self, request):
        """
        get:
        The get articles endpoint
        """
        page_limit = request.GET.get('limit')

        if not page_limit or not page_limit.isdigit():
            page_limit = 9

        queryset = self.queryset
        paginator = PageNumberPagination()
        paginator.page_size = page_limit

        page = paginator.paginate_queryset(queryset, request)
        serializer = ArticleSerializer(page, many=True,
                                       context={'request': request})

        dictionary = None
        data = []
        for article in serializer.data:
            dictionary = dict(article)
            dictionary = add_social_share(dictionary)
            dictionary['author'] = user_object(dictionary['author'])
            data.append(dictionary)

        return paginator.get_paginated_response(data=data)

    def retrieve(self, request, slug=None):
        """
        get:
        The get an article endpoint
        """
        try:
            article = ArticleModel.objects.filter(slug=slug)[0]
        except:
            return JsonResponse({"status": 404,
                                 "error": "Article with slug {} not found".format(slug)},
                                status=404)
        serializer = ArticleSerializer(article,
                                       context={'request': request})
        response = Response(serializer.data)
        response.data['author'] = user_object(serializer.data['author'])
        response.data = add_social_share(response.data)
        return JsonResponse({"status": 200,
                             "data": response.data},
                            status=200)

    def update(self, request, slug=None, *args, **kwargs):
        """
        put:
        The update article endpoint
        """
        request.POST._mutable = True
        try:
            article = ArticleModel.objects.filter(slug=slug)[0]
        except:
            return JsonResponse(
                {"status": 404,
                 "error": "Article with slug {} not found".format(slug)},
                status=404)
        serializer = ArticleSerializer(article,
                                       context={'request': request})

        if not article.author.id == request.user.id:
            return JsonResponse(
                {"status": 403,
                 "error": "You cannot edit an article you do not own"},
                status=403)

        body = request.data.get('body')
        read_time = readtime.of_text(body)
        request.data['readtime'] = read_time.text
        serializer = ArticleSerializer(article,
                                       data=request.data,
                                       context={'request': request},
                                       partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response(serializer.data)
        response.data['author'] = user_object(serializer.data['author'])
        response.data = add_social_share(response.data)
        return Response({"status": 201,
                         "data": response.data},
                        status=201)

    def destroy(self, request, slug=None, *args, **kwargs):
        """
        delete:
        The delete article endpoint
        """
        try:
            article = ArticleModel.objects.filter(slug=slug)[0]

            if not article.author.id == request.user.id:
                return Response({'status': 403, 'error': "You cannot delete an article you do not own"}, status=403)

            self.perform_destroy(article)
            return Response({'status': 200,
                             'data': 'Article deleted successfully'},
                            status=200)
        except:
            return JsonResponse(
                {'status': 404,
                 'error': 'Article with slug {} not found'.format(slug)},
                status=404)

    def create_article(self, request):
        """
        Function for creating an article
        """
        request.data['author'] = request.user.id

        body = request.data.get('body')
        read_time = readtime.of_text(body)
        request.data['readtime'] = read_time.text

        serializer = ArticleSerializer(data=request.data,
                                       context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = serializer.data

        response['author'] = user_object(response['author'])
        response = add_social_share(response)
        return Response({"status": 201, "data": response}, status=201)

    def check_if_duplicate(self, userid, title1, body1):

        records = ArticleModel.objects.filter(
            author_id=userid)

        duplicate_record = records.filter(
            title=title1.strip()).filter(
            body=body1.strip()
        )
        if duplicate_record.exists():
            return True
        return False

    def upload_image(self, request):
        """
        Function for uploading image
        """
        cloud_response = ImageUploader(request.FILES['image'])
        if cloud_response is not None:
            if cloud_response.get('error', False):
                return Response(cloud_response, status=int(cloud_response.get('status')))

            image_url = cloud_response.get(
                'secure_url', request.FILES['image'])
            request.data['image'] = image_url
            return self.create_article(request)


class CommentView(viewsets.ModelViewSet):
    """
    The Comment view
    """
    queryset = FluentComment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'slug'

    def create(self, request, *args, **kwargs):
        """
        post:
        The create a comment endpoint
        """
        if request.user.is_authenticated:

            data = self.request.data
            comment = data['comment']

            slug = self.kwargs.get('slug')
            slug_exists = ArticleModel.objects.filter(slug=slug)
            if not slug_exists:
                return JsonResponse(
                    {'status': 404,
                     'error': 'Article with slug {} not found'.format(slug)},
                    status=404)

            parent = request.GET.get('parent_id')
            if parent:
                parent_exists = FluentComment.objects.filter(
                    pk=parent, object_pk=slug)
                if not parent_exists:
                    return JsonResponse(
                        {'status': 404,
                         'error': 'No comment with id {} found for article with slug {}'.format(parent, slug)},
                        status=404)

            submit_date = timezone.now()
            content = ContentType.objects.get(model='user').pk
            comment = FluentComment.objects.create(object_pk=slug,
                                                   comment=comment,
                                                   submit_date=submit_date,
                                                   content_type_id=content,
                                                   user_id=self.request.user.id,
                                                   site_id=settings.SITE_ID,
                                                   parent_id=parent)

            user = User.objects.filter(pk=self.request.user.id).first()
            CommentModel.objects.create(comment_id=comment.id, user=user)

            serializer = CommentSerializer(
                comment, context={'request': request})

            response = Response(serializer.data)
            response.data['author'] = user_object(request.user.id)
            del response.data['user_id']
            return Response(response.data,
                            status=status.HTTP_201_CREATED)

    def update(self, request, slug=None):
        """
        put:
        Update a comment endpoint
        """

        if request.user.is_authenticated:
            slug = self.kwargs.get('slug')
            queryset = get_comment_queryset(request, slug)
            comment_id = request.GET.get('id')

            if not queryset:
                response = {
                    'error': 'No comment with id {} found for article '
                             'with slug {}'.format(comment_id, slug)
                }
                return Response(data=response, status=status.HTTP_404_NOT_FOUND)

            old_comment = queryset.comment
            if queryset.user != request.user:
                response = {
                    'error': 'You cannot update a comment you do not own.'
                }
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

            if request.data['comment'] == old_comment:
                response = {
                    'error': 'This is the current comment'
                }
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

            comment, created = CommentHistoryModel.objects.get_or_create(
                updated_comment=old_comment, comment=queryset)
            serializer = CommentSerializer(
                queryset, request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = Response(serializer.data)
            response.data['author'] = user_object(request.user.id)
            del response.data['user_id']
            return Response({"data": response.data})

    def list(self, request, *args, **kwargs):
        """
        get:
        The list all comments for an article endpoint
        """
        slug = self.kwargs.get('slug')
        slug_exists = ArticleModel.objects.filter(slug=slug)
        if not slug_exists:
            return JsonResponse(
                {'status': 404,
                 'error': 'Article with slug {} not found'.format(slug)},
                status=404)

        queryset = FluentComment.objects.filter(object_pk=slug)
        serializer = CommentSerializer(queryset, many=True)

        if queryset.count() == 0:
            return JsonResponse(
                {'status': 404,
                 'error': "No comments yet on this article".format(slug)},
                status=404)

        if queryset.count() == 1:
            comment_votes = CommentModel.objects.filter(
                comment=queryset.first().id).first()

            response = Response(serializer.data)
            response = dict(response.data[0].items())
            response['author'] = user_object(response['user_id'])
            response['votes'] = comment_votes.vote_score
            response['num_vote_down'] = comment_votes.num_vote_down
            response['num_vote_up'] = comment_votes.num_vote_up
            del response['user_id']
            return Response({"Comment": response})

        data = configure_response(serializer)
        return Response(
            {"Comments": data,
             "commentsCount": queryset.count()})


class CommentLikeView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        comment_id = self.kwargs.get('id')

        check_article(slug)

        comment_exists = CommentModel.objects.filter(
            comment=comment_id).first()
        if not comment_exists:
            return JsonResponse(
                {'status': 404,
                 'error': 'Comment with id {} not found'.format(comment_id)},
                status=404)

        check_vote = comment_exists.votes.exists(request.user.id)

        if check_vote:
            comment_exists.votes.delete(request.user.id)
            return JsonResponse({
                "status": 200,
                "message": "You have deleted this like", },
                status=200)
        comment_exists.votes.up(request.user.id)

        return JsonResponse({
            "status": 200,
            "message": "You have liked this comment", },
            status=200)


class CommentDisLikeView(GenericAPIView):
    """The like view for articles"""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        comment_id = self.kwargs.get('id')

        check_article(slug)

        comment_exists = CommentModel.objects.filter(
            comment=comment_id).first()

        if not comment_exists:
            return JsonResponse(
                {'status': 404,
                 'error': 'Comment with id {} not found'.format(comment_id)},
                status=404)

        vote_down = comment_exists.votes.down(request.user.id)

        if vote_down:
            return JsonResponse({"status": 200,
                                 "message": "You have Disliked this comment", },
                                status=200)
        comment_exists.votes.delete(request.user.id)
        return JsonResponse({"status": 200,
                             "message": "You have deleted this dislike", },
                            status=200)


class LikeView(GenericAPIView):
    """The like view for articles"""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')

        slug_exists = ArticleModel.objects.filter(slug=slug)
        if not slug_exists:
            return JsonResponse(
                {'status': 404,
                 'error': 'Article with slug {} not found'.format(slug)},
                status=404)

        article = ArticleModel.objects.filter(slug=slug)[0]

        user_id = request.user.id
        check_vote = article.votes.exists(user_id)

        if check_vote:
            article.votes.delete(user_id)
            return JsonResponse({
                "status": 200,
                "message": "You have deleted this like", },
                status=200)
        article.votes.up(user_id)

        return JsonResponse({"status": 200,
                             "message": "You have liked this article",
                             },
                            status=200)


class DisLikeView(GenericAPIView):
    """The like view for articles"""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')

        slug_exists = ArticleModel.objects.filter(slug=slug)
        if not slug_exists:
            return JsonResponse(
                {'status': 404,
                 'error': 'Article with slug {} not found'.format(slug)},
                status=404)

        article = ArticleModel.objects.filter(slug=slug)[0]
        user_id = request.user.id

        vote_down = article.votes.down(user_id)

        if vote_down:
            return JsonResponse({"status": 200,
                                 "message": "You have Disliked this article", },
                                status=200)
        article.votes.delete(user_id)
        return JsonResponse({"status": 200,
                             "message": "You have deleted this dislike", },
                            status=200)


class FavoriteArticle(viewsets.ModelViewSet):
    """Favorite an article"""
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteArticleSerializer

    def create(self, request, *args, **kwargs):
        """
        post:
        Create favorite endpoint
        """
        slug = self.kwargs.get('slug')
        article = ArticleModel.objects.all().filter(slug=slug).first()
        user = request.user

        if article is None:
            response = {
                'error': 'Article with slug {} not found'.format(slug)
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)

        if user == article.author:
            response = {
                "error": "You are not allowed to favourite your own article"
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        try:
            existing_favorite = FavoriteArticleModel.objects.get(
                article=article, favoritor=request.user)
            serializer = self.serializer_class(
                existing_favorite, data=request.data)
        except FavoriteArticleModel.DoesNotExist:
            serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(article=article, favoritor=user)

        return Response({
            "data": serializer.data
        })

    def list(self, request, slug):
        """
        get:
        The get all articles favorited endpoint
        """
        querysets = FavoriteArticleModel.objects.filter(favoritor=request.user)
        data = []
        for queryset in querysets:
            serializer = FavoriteArticleSerializer(queryset)
            article = serializer.data
            data.append(article)
        return Response({'data': data})

    def destroy(self, request, slug=None, *args, **kwargs):
        """
        delete:
        Unfavorite article endpoint
        """
        try:
            article = ArticleModel.objects.filter(slug=slug).first()
            existing_favorite = FavoriteArticleModel.objects.get(
                article=article, favoritor=request.user)
            self.perform_destroy(existing_favorite)
            return Response({'status': 200,
                             'data': 'Article unfavorited successfully'},
                            status=200)
        except:
            response = {
                'error': 'Article with slug {} not found'.format(slug)
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)


class ArticleList(ListAPIView):
    """
    Search and filter View
    """
    permission_classes = [AllowAny]
    queryset = ArticleModel.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    filter_class = ArticleFilter
    search_fields = ('author__username', 'description', 'body', 'title', )

    def list(self, request):
        # with filter
        queryset = self.filter_queryset(self.get_queryset())

        # pagination
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        dictionary = None
        data = []
        if serializer.data:
            for article in serializer.data:
                dictionary = dict(article)
                dictionary = add_social_share(dictionary)
                dictionary['author'] = user_object(dictionary['author'])
                data.append(dictionary)
            return self.get_paginated_response(data=data)
        return Response({'status': 404, 'message': 'We could not find what you are looking for.'}, status=404)


class CommentHistory(ListAPIView):
    """
    Get edit history of a comment.
    """
    permission_classes = [AllowAny]
    serializer_class = CommentHistorySerializer

    def list(self, request, *args, **kwargs):
        comment_id = self.kwargs.get('id')
        queryset = CommentHistoryModel.objects.all()
        history = queryset.filter(comment_id=comment_id)
        if history.count() < 1:
            return Response({"message": "This comment has not been edited"},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookmarkArticleView(viewsets.ModelViewSet):
    """Bookmark an article"""
    permission_classes = [IsAuthenticated]
    serializer_class = BookmarkArticleSerializer

    def create(self, request, *args, **kwargs):
        """
        post:
        Create bookmark endpoint
        """
        slug = self.kwargs.get('slug')
        article = ArticleModel.objects.all().filter(slug=slug).first()
        user = request.user

        if article is None:
            response = {
                'error': 'Article with slug {} not found'.format(slug)
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)

        if user == article.author:
            response = {
                "error": "You cannot bookmark your own article"
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        try:
            bookmarked_article = BookmarkArticleModel.objects.get(
                article=article, user=request.user)

            if bookmarked_article:
                response = {
                    "error": "You already bookmarked this article"
                }
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        except BookmarkArticleModel.DoesNotExist:
            serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(article=article, user=user)
        response = {
            "data": serializer.data
        }
        return Response(data=response, status=status.HTTP_200_OK)

    def list(self, request, slug):
        """
        get:
        The get all articles bookmarked endpoint
        """
        querysets = BookmarkArticleModel.objects.filter(user=request.user)
        data = []
        serializer = BookmarkArticleSerializer(querysets)
        for queryset in querysets:
            serializer = BookmarkArticleSerializer(queryset)
            article = serializer.data
            data.append(article)
        response = {
            "data": data
        }
        return Response(data=response, status=status.HTTP_200_OK)

    def destroy(self, request, slug=None):
        """
        delete:
        The unbookmark article endpoint
        """
        try:
            article = ArticleModel.objects.filter(slug=slug).first()
            bookmarked_article = BookmarkArticleModel.objects.get(
                article=article, user=request.user)
            self.perform_destroy(bookmarked_article)
            response = {
                "data": "Article unbookmarked successfully"
            }
            return Response(data=response, status=status.HTTP_200_OK)
        except:
            response = {
                'error': 'Article with slug {} not found'.format(slug)
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)


class TagViewSet(APIView):
    """Add tags to an article"""
    pagination_class = None

    def get(self, request):
        """
        get:
        The get all tags endpoint
        """

        queryset = TagModel.objects.all()
        serializer = TagSerializer(queryset, many=True)
        return Response({'Tags': serializer.data})
