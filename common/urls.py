# from django.template.defaulttags import url
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from django.urls import include, path, re_path
from common import views
from common.views import ImageUploadViewSet

router = routers.DefaultRouter()
router.register('user', views.UserViewSet)

app_name = 'common'

urlpatterns = [
    path('', include(router.urls)),

    path('user/login', views.UserLoginViewSet.as_view()),
    path('user/logout', views.UserLogoutViewSet.as_view()),
    path('user/pwd', views.PasswordUpdateViewSet.as_view()),
    re_path(r'upload/$', ImageUploadViewSet.as_view()),
]
