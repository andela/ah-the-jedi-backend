from django.urls import path, include
from rest_framework import routers
from .views import ArticleView, CommentView, LikeView, DisLikeView, FavoriteArticle


router = routers.DefaultRouter()
router.register('articles', ArticleView)

urlpatterns = [
    path('', include(router.urls)),
    path('articles/<slug>/comments/', CommentView.as_view({'post': 'create',
                                                           'get': 'list'})),
    path('articles/<slug>/like/', LikeView.as_view()),
    path('articles/<slug>/dislike/', DisLikeView.as_view()),
    path('articles/<slug>/favorite/', FavoriteArticle.as_view({'post': 'create',
                                                               'get': 'list',
                                                               'delete': 'destroy'})),
]
