from articles.api.views import ArticleViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register('', ArticleViewSet, base_name='articles')
urlpatterns = [
    path('', include(router.urls)),
    path('game/test/', views.test_json, name='test')
]

# from django.urls import path

# from .views import (
#     ArticleListView,
#     ArticleDetailView,
#     ArticleCreateView,
#     ArticleUpdateView,
#     ArticleDeleteView
# )
#
#
# urlpatterns = [
#     path('', ArticleListView.as_view()),
#     path('create/', ArticleCreateView.as_view()),
#     path('<pk>', ArticleDetailView.as_view()),
#     path('<pk>/update/', ArticleUpdateView.as_view()),
#     path('<pk>/delete/', ArticleDeleteView.as_view())
# ]