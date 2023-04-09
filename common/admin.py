from django.contrib import admin

# Register your models here.
from common.models import User, OpLogs, AccessTimeOutLogs


@admin.register(User)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'avatar', 'email', 'is_active', 'created_at', 'nickname']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # queryset = queryset.prefetch_related(
        #     'ansible_log', 'playbook_user', 'admin_record',
        #     'playbook_log', 'ansilbe_role', 'bgbu')
        return queryset

@admin.register(OpLogs)
class OpLogsAdmin(admin.ModelAdmin):
    list_display = ['re_url', 're_method', 'access_time', 're_ip', 'user_agent', 'rp_code', 're_content', 're_time',
                    're_user',
                    ]  # rp_content 响应参数内容太多不展示
    list_filter = ('re_url', 're_user')
    search_fields = ['re_url', 're_user', 'rp_code']


@admin.register(AccessTimeOutLogs)
class AccessTimeOutLogsAdmin(admin.ModelAdmin):
    list_display = ['re_url', 're_method', 'access_time', 're_ip', 'user_agent', 'rp_code', 're_content', 're_time',
                    're_user',
                    ]  # rp_content 响应参数内容太多不展示
    list_filter = ('re_url', 're_user')
    search_fields = ['re_url', 're_user', 'rp_code']