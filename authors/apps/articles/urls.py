from django.urls import path, include
from rest_framework import routers
from .views import (ArticleView, CommentView, LikeView,
                    DisLikeView, FavoriteArticle, ArticleList,
                    BookmarkArticleView, TagViewSet, CommentLikeView, CommentDisLikeView, CommentHistory)


router = routers.DefaultRouter()
router.register('articles', ArticleView)

urlpatterns = [
    path('', include(router.urls)),
    path('articles/<slug>/comments/', CommentView.as_view({'post': 'create',
                                                           'get': 'list',
                                                           'put': 'update'})),
    path('articles/<slug>/comments/<id>/like/', CommentLikeView.as_view()),
    path('articles/<slug>/comments/<id>/dislike/', CommentDisLikeView.as_view()),
    path('articles/<slug>/like/', LikeView.as_view()),
    path('articles/<slug>/dislike/', DisLikeView.as_view()),
    path('articles/<slug>/favorite/', FavoriteArticle.as_view({'post': 'create',
                                                               'get': 'list',
                                                               'delete': 'destroy'})),
    path('article/search/', ArticleList.as_view(), name='article-search'),
    path('articles/<slug>/bookmark/', BookmarkArticleView.as_view({'post': 'create',
                                                                   'get': 'list',
                                                                   'delete': 'destroy'})),
    path('tags/', TagViewSet.as_view()),
    path('articles/<slug>/comments/<int:id>/history/', CommentHistory.as_view())
]
