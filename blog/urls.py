from django.urls import include, path
from rest_framework import routers

from blog import views

router = routers.DefaultRouter()
router.register('article', views.ArticleViewSet)
router.register('list', views.ArticleListViewSet)
router.register('publish', views.ArticlePublishViewSet)
router.register('offline', views.ArticleOfflineViewSet)
router.register('archive', views.ArticleArchiveListViewSet)
router.register('tag', views.TagViewSet)
router.register('category', views.CatalogViewSet)
router.register('catalog', views.CatalogViewSet)
router.register('comment', views.CommentViewSet)
router.register('like', views.LikeViewSet)
router.register('message', views.MessageViewSet)
router.register('number', views.NumberViewSet)
router.register('top', views.TopArticleViewSet)

app_name = 'blog'

urlpatterns = [
    path('', include(router.urls)),
]
