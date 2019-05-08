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
from rest_framework_swagger.views import get_swagger_view


articles_urls = include('authors.apps.articles.urls')
authentication_urls = include('authors.apps.authentication.urls')

swagger_view = get_swagger_view(title='The Jedi Authors Haven API')

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
    path('', swagger_view, name="root_url"),
    path('api/', include(('authors.apps.highlights.urls',
                          'highlights'), namespace='highlights')),
]
