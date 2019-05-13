from django.urls import path
from .views import HighlightArticleView

app_name = "highlights"

urlpatterns = [
    path("articles/<slug>/highlight/",
         HighlightArticleView.as_view(), name='highlight')

]
