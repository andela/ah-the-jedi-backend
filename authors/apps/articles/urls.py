from django.urls import path, include
from rest_framework import routers
from .views import ArticleView, CommentView


router = routers.DefaultRouter()
router.register('articles', ArticleView)

urlpatterns = [
    path('', include(router.urls)),
    path('articles/<slug>/comments/', CommentView.as_view({'post': 'create', 'get': 'list'})),
]
