from django.contrib import admin

# Register your models here.
from blog.models import Tag, Catalog, Article, Comment


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'modified_at']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # queryset = queryset.prefetch_related(
        #     'ansible_log', 'playbook_user', 'admin_record',
        #     'playbook_log', 'ansilbe_role', 'bgbu')
        return queryset


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # queryset = queryset.prefetch_related(
        #     'ansible_log', 'playbook_user', 'admin_record',
        #     'playbook_log', 'ansilbe_role', 'bgbu')
        return queryset


@admin.register(Article)
class ArticleListAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'excerpt', 'cover', 'created_at', 'modified_at',
                    'catalog', 'views', 'comments', 'words', 'likes', 'status', ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # queryset = queryset.prefetch_related(
        #     'ansible_log', 'playbook_user', 'admin_record',
        #     'playbook_log', 'ansilbe_role', 'bgbu')
        return queryset


@admin.register(Comment)
class ArticleListAdmin(admin.ModelAdmin):
    list_display = ['id', 'user','article', 'created_at', 'reply', 'content' ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # queryset = queryset.prefetch_related(
        #     'ansible_log', 'playbook_user', 'admin_record',
        #     'playbook_log', 'ansilbe_role', 'bgbu')
        return queryset
