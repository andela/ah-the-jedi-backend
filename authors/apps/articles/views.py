from django.shortcuts import render
from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import permission_classes
from .serializers import ArticleSerializer, TABLE
from django.contrib.auth.models import User
from ..authentication.models import User
from .models import ArticleModel
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser, AllowAny
)
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import json
from django.http.response import Http404
import smtplib
from django.conf import settings
from .utils import ImageUploader
from django.apps import apps


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
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def create(self, request):
        """
        post:
        The create article endpoint
        """
        userid = request.user.id
        title = request.data['title']
        body = ''

        try:
            body = request.data['body']
        except:
            pass

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
        The get article endpoint
        """
        queryset = self.queryset
        serializer = ArticleSerializer(queryset, many=True,
                                       context={'request': request})
        dictionary = None
        data = []
        for article in serializer.data:
            dictionary = dict(article)
            dictionary['author'] = self.user_object(dictionary['author'])
            data.append(dictionary)

        return JsonResponse({"status": 200,
                             "data": data},
                            status=200)

    def retrieve(self, request, slug=None):
        """
        get:
        The get an article endpoint
        """
        try:
            article = ArticleModel.objects.filter(slug=slug)[0]
        except:
            return JsonResponse({"status": 404,
                                 "error": "Intervention with slug {} not found".format(slug)},
                                status=404)
        serializer = ArticleSerializer(article,
                                       context={'request': request})
        response = Response(serializer.data)
        response.data['author'] = self.user_object(serializer.data['author'])
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

        request.data['slug'] = request.data['title']
        serializer = ArticleSerializer(article,
                                       data=request.data,
                                       context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response(serializer.data)
        response.data['author'] = self.user_object(serializer.data['author'])
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
        response = super().create(request)
        response.data['author'] = self.user_object(response.data['author'])
        return Response({"status": 201, "data": response.data}, status=201)

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

    def user_object(self, uid):
        """
        Function for getting user object
        """
        instance = User.objects.filter(id=uid)[0]

        user = {
            'id': instance.id,
            'email': instance.email,
            'username': instance.username,
        }

        try:
            user.bio = instance.bio
        except:
            pass
        try:
            user.following = instance.following
        except:
            pass
        try:
            user.image = instance.image
        except:
            pass

        return user
