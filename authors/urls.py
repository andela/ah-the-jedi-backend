"""authors URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="The Jedi Authors Haven API",
        default_version='v1',
        description=(
            "We have a vision to create a community of "
            "like minded authors to foster inspiration "
            "and innovation by leveraging the modern web."),
        contact=openapi.Contact(email="<jedi.authors.haven@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


articles_urls = include('authors.apps.articles.urls')
authentication_urls = include('authors.apps.authentication.urls')
notification_urls = include('authors.apps.notifications.urls')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(('authors.apps.authentication.urls',
                          'authentication'), namespace='authentication')),
    path('api/', include(('authors.apps.profiles.urls',
                          'profiles'), namespace='profiles')),
    path('api/', authentication_urls),
    path('api/', articles_urls),
    path('api/users/social/', include('rest_framework_social_oauth2.urls')),
    path('api/', include(('authors.apps.follows.urls',
                          'follows'), namespace='follows')),
    path('api/', include('authors.apps.ratings.urls')),
    path('api/', notification_urls),
    path('api/', include(('authors.apps.highlights.urls',
                          'highlights'), namespace='highlights')),
    path('', schema_view.with_ui('swagger',
                                 cache_timeout=0),
         name='schema-swagger-ui'),
]
