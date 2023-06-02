from django.urls import include, path
from rest_framework import routers

from blog import views

router = routers.DefaultRouter()
router.register(r'article', views.ArticleViewSet)
router.register(r'list', views.ArticleListViewSet)
router.register(r'publish', views.ArticlePublishViewSet)
router.register(r'offline', views.ArticleOfflineViewSet)
router.register(r'archive', views.ArticleArchiveListViewSet)
router.register(r'tag', views.TagViewSet)
router.register(r'category', views.CatalogViewSet)
router.register(r'catalog', views.CatalogViewSet)
router.register(r'comment', views.CommentViewSet)
router.register(r'like', views.LikeViewSet)
router.register(r'message', views.MessageViewSet)
router.register(r'number', views.NumberViewSet)
router.register(r'top', views.TopArticleViewSet)

app_name = 'blog'

urlpatterns = [
    path('', include(router.urls)),
]
