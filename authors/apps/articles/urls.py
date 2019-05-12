from django.urls import path, include
from rest_framework import routers
from .views import (ArticleView, CommentView, LikeView,
                    DisLikeView, FavoriteArticle, ArticleList,
                    BookmarkArticleView, TagViewSet)


router = routers.DefaultRouter()
router.register('articles', ArticleView)
# router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('articles/<slug>/comments/', CommentView.as_view({'post': 'create',
                                                           'get': 'list'})),
    path('articles/<slug>/like/', LikeView.as_view()),
    path('articles/<slug>/dislike/', DisLikeView.as_view()),
    path('articles/<slug>/favorite/', FavoriteArticle.as_view({'post': 'create',
                                                               'get': 'list',
                                                               'delete': 'destroy'})),
    path('article/search/', ArticleList.as_view(), name='article-search'),
    path('articles/<slug>/bookmark/', BookmarkArticleView.as_view({'post': 'create',
                                                                   'get': 'list',
                                                                   'delete': 'destroy'})),
    path('tags/', TagViewSet.as_view({'get': 'list',
                                      'post': 'create'})),
]
