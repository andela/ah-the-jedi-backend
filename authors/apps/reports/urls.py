from django.urls import path, include
from rest_framework import routers
from .views import ReportView, ReportList, DeleteView, ArticleDeleteView


router = routers.DefaultRouter()
router.register('reports', ReportView)

urlpatterns = [
    path('', include(router.urls)),
    path('report/get_all/', ReportList.as_view(), name='get_all'),
    path('report/delete/<id>/', DeleteView.as_view(), name='delete'),
    path('articles/delete/<slug>/',
         ArticleDeleteView.as_view(), name='article_delete'),
]
