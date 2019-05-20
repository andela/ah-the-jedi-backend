"""
Helper functions and classes for articles
"""
import datetime
import re
import cloudinary.uploader
from django_filters import (
    FilterSet, rest_framework)
from rest_framework import serializers
from fluent_comments.models import FluentComment
from rest_framework.exceptions import (ValidationError, NotFound)
from .models import (ArticleModel, TagModel,
                     CommentModel, ReadStatsModel, User)


def ImageUploader(image):
    """
    Upload image to cloudinary
    :param image: FILE from post request
    :return: uploaded image data if image was uploaded successfully else None
    """

    if not str(image.name).endswith(('.png', '.jpg', '.jpeg')):
        return {"status": 400, "error": ["Ensure that the file is an image"]}

    try:
        image_data = cloudinary.uploader.upload(
            image,
            public_id=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                          .replace("-", "")
                          .replace(":", "")
                          .replace(" ", "")),
            crop='limit',
            width=2000,
            height=2000,
            eager=[
                {'width': 200, 'height': 200,
                 'crop': 'thumb', 'gravity': 'face',
                 'radius': 20, 'effect': 'sepia'},
                {'width': 100, 'height': 150,
                 'crop': 'fit', 'format': 'png'}
            ]
        )
        return image_data

    except Exception as e:
        return {"status": e.status_code,
                "error": e.__dict__}


def user_object(uid):
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


def configure_response(serializer):
    """Function to configure response with a user information"""

    dictionary = None
    data = []
    for comment in serializer.data:
        dictionary = dict(comment)

        comment_votes = CommentModel.objects.filter(
            comment=dictionary['id']).first()

        dictionary['author'] = user_object(dictionary['user_id'])
        if comment_votes:
            dictionary['votes_score'] = comment_votes.vote_score
            dictionary['num_vote_down'] = comment_votes.num_vote_down
            dictionary['num_vote_up'] = comment_votes.num_vote_up
        del dictionary['user_id']
        data.append(dictionary)
    return data


def add_social_share(request):
    """
    Function for adding share url to an article
    """
    request['twitter'] = 'https://twitter.com/share?url=' + \
        request['url']+'&amp;text=Checkout this article on ' + \
        request['title']
    request['facebook'] = 'http://www.facebook.com/sharer.php?u=' + \
        request['url']+'&quote=Checkout this article on ' + \
        request['title']
    request['mail'] = 'mailto:?subject=Checkout this article on {} read&body={}'.format(
        request['title'], request['url'])

    return request


def save_read_stat(request, article):
    """ Save a read statitic to db if it does not exist"""
    if not request.user.is_anonymous:
        existing_read = ReadStatsModel.objects.all().filter(
            user=request.user, article=article
        )

        if not existing_read:
            ReadStatsModel.objects.create(
                user=request.user, article=article)


class ArticleFilter(FilterSet):
    """
    Custom filter class for articles
    """
    title = rest_framework.CharFilter('title',
                                      lookup_expr='icontains')
    author = rest_framework.CharFilter('author__username',
                                       lookup_expr='icontains')
    tag = rest_framework.CharFilter('tagList',
                                    lookup_expr='iexact',
                                    method='m2mfilter')

    class Meta:
        model = ArticleModel
        fields = ("title", "author", "tag")

    def m2mfilter(self, qs, tags, value):
        """
        Custom filter for the manytomany tagList field
        """

        if not value:
            return qs

        values = value.split(',')
        return qs.filter(tagList__tagname__in=values).distinct()


class TagField(serializers.RelatedField):
    """
    Custom related field for the tags field to ensure a tags table
    is created on article creation
    """

    def get_queryset(self):

        return TagModel.objects.all()

    def to_representation(self, value):
        """
        Return the representation that should be used to serialize the field
        """
        return value.tagname

    def to_internal_value(self, data):
        """
        Validate data and restore it back into its internal
        python representation
        """

        if data:
            if not re.match(r'^[a-zA-Z0-9][ A-Za-z0-9_-]*$', data):
                raise ValidationError(
                    detail={'message': "{} is an invalid tag".format(data)})

            tag, created = TagModel.objects.get_or_create(tagname=data)
            return tag


def get_comment_queryset(request, slug):
    article = ArticleModel.objects.filter(slug=slug).first()
    if article is None:
        response = {
            'error': 'Article with slug {} not found'.format(slug)
        }
        raise NotFound(response)

    comment_id = request.GET.get('id')

    if not comment_id:
        response = {
            'error': 'Please enter a comment id'
        }
        raise ValidationError(response)

    try:
        queryset = FluentComment.objects.get(
            pk=comment_id, object_pk=slug)
    except FluentComment.DoesNotExist:
        queryset = None

    return queryset


def check_article(slug):
    """
    Function that checks if an article exists
    """
    slug_exists = ArticleModel.objects.filter(slug=slug)
    if not slug_exists:
        raise NotFound(
            {'status': 404,
             'error': 'Article with slug {} not found'.format(slug)})
    else:
        return True
