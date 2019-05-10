import os

from django.core.mail import EmailMessage, get_connection
from django.template.loader import render_to_string
from rest_framework.exceptions import NotFound, PermissionDenied

from . import models
from ..authentication.models import User
from ..articles.models import ArticleModel, FavoriteArticleModel
from ..authentication.messages import errors

domain = os.getenv('DOMAIN')


def make_update(instance, validated_data):
    """
    Performs an update on an instance
    """

    for (key, value) in validated_data.items():

        setattr(instance, key, value)

    instance.save()

    return instance


def get_notification(user, read=None, single=False):
    """
    This method 'get_notifications'
    fetches all instances of notification
    for a specific user if any
    """

    response = (models.Notifications.objects.filter(user=user, read=read)
                if read is not None
                else models.Notifications.objects.filter(user=user))

    if single:

        response = models.Notifications.objects.filter(id=user).first()

    return response


def get_subscriptions(user):
    """
    This method 'get_subscriptions'
    fetches all instances of subscriptions
    for a specific user
    """

    return models.Subscriptions.objects.get(user=user)


def get_user(username):
    """
    This method 'get_user' fetches
    instance of the user if it exists
    """

    return User.objects.filter(username=username).first()


def fetch_favorites(article):
    """
    This method 'fetch_favorites'
    fetches all instances of article
    favorites by users if any
    """

    return FavoriteArticleModel.objects.filter(article=article)


def fetch_articles(slug):
    """
    This method 'fetch_article'
    fetches an instances of an article
    if any
    """

    return ArticleModel.objects.filter(slug=slug).first()


def fetch_user(username):
    """
    This method 'fetch_user'
    fetches an instances of an user
    if any
    """

    return User.objects.get(username=username)


def check_is_object_owner(requester, user):
    """
    This method 'check_is_object_owner'
    raises Forbidden if not object owner
    """

    if not requester.user == user.user:

        raise PermissionDenied(errors["not_owner"])


def fetch_unsubscriptions(app=''):
    """
    This method 'fetch_unsubscriptions'
    fetches an instances of excluded
    users subscriptions
    """

    mail_exclude = models.Subscriptions.objects.filter(email=False)

    mail_exclude = [fetch_user(
        username=user.user.username).email for user in mail_exclude]

    app_exclude = models.Subscriptions.objects.filter(app=False)

    app_exclude = [fetch_user(
        username=user.user.username).email for user in app_exclude]

    return app_exclude if app else mail_exclude


def send_mail_notification(recipients, msg=''):
    """
    Sends email for notifications
    """

    msg = EmailMessage("ACTIVITY UPDATE",
                       msg, "Authors Haven", bcc=recipients)

    msg.content_subtype = "html"
    msg.send()


def save_notifications(username, message, url):
    """
    Format and save notifications
    """

    user = username and User.objects.filter(
        username=username).first() or None

    models.Notifications(user=user,
                         message=message,
                         url=url).save()


def make_message(author, title, url='', opt_url='', comment=False, html=False):
    """
    Creates and returns a message
    based on the provided params
    """

    message = comment and "responded to" or "created a new article"

    response = "{} {} '{}'.".format(author, message, title)

    dictionary = comment and ("NEW COMMENT", "View Comment") or (
        "NEW ARTICLE", "View Article")

    html_message = render_to_string("notify.html", {
        "heading": dictionary[0],
        "message": response,
        "url": url,
        "action_text": dictionary[1],
        "opt_url": opt_url
    })

    return html_message if html else response


def make_notifications(username, title, slug, obj, comment=False):
    """
    Save notification and send email
    """

    url, opt_url = (
        "{}/api/articles/{}/".format(domain, slug),
        "{}/api/notifications/subscriptions".format(domain))

    mail_exlude, app_exclude = (
        fetch_unsubscriptions(), fetch_unsubscriptions(True))

    message, html_message, mails = (
        make_message(username, title, comment=comment),
        make_message(username, title,
                     url, opt_url,
                     comment, True),
        ''
    )

    if comment:

        [save_notifications(favorite.favoritor.username, message, url)
         for favorite in obj if favorite.favoritor.email not in app_exclude]

        mails = [fetch_user(username=favorite.favoritor.username).email
                 for favorite in obj if favorite.favoritor.email
                 not in mail_exlude]

    else:

        [save_notifications(user.follower.username, message, url)
         for user in obj if user.follower.email not in app_exclude]

        mails = [fetch_user(username=user.follower.username).email
                 for user in obj if user.follower.email not in mail_exlude]

    send_mail_notification(mails, html_message)


def create_post_notification(sender, **kwargs):
    """
    Create notification if followed users create article
    """

    article, author = kwargs["instance"], kwargs["instance"].author

    followers = author.followers.all()

    make_notifications(author.username, article.title, article.slug, followers)


def create_comment_notification(sender, **kwargs):
    """
    Create notification if users comments on favorited article
    """

    slug, username = (
        kwargs["instance"].object_pk,
        kwargs["instance"].user.username)

    article = fetch_articles(slug=slug)

    favorites = fetch_favorites(article=article)

    make_notifications(username, article.title, slug, favorites, True)


def create_subscriptions(sender, **kwargs):
    """
    Create an instance of user subscriptions
    in the Subscriptions model
    """

    if kwargs['created']:

        models.Subscriptions.objects.create(user=kwargs["instance"])
