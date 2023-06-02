from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('common/', include('common.urls', namespace='common')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'upload/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
]
