# from django.contrib.auth.models import AbstractUserfrom
from django.contrib.auth.models import AbstractUser
from django.db import models


class AbstractBaseModel(models.Model):
    creator = models.IntegerField('creator', null=True)
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)

    modifier = models.IntegerField('modifier', null=True)
    modified_at = models.DateTimeField(verbose_name='Modified at', auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, AbstractBaseModel):
    avatar = models.CharField('头像', max_length=1000, blank=True)
    nickname = models.CharField('昵称', null=True, blank=True, max_length=200)

    class Meta(AbstractUser.Meta):
        db_table = 'blog_user'
        swappable = 'AUTH_USER_MODEL'


class OpLogs(models.Model):
    '''操作日志表'''
    id = models.AutoField(primary_key=True)
    re_time = models.CharField(max_length=32, verbose_name='请求时间')
    re_user = models.CharField(max_length=32, verbose_name='操作人')
    re_ip = models.CharField(max_length=32, verbose_name='请求IP')
    re_url = models.CharField(max_length=255, verbose_name='请求url')
    re_method = models.CharField(max_length=11, verbose_name='请求方法')
    re_content = models.TextField(null=True, verbose_name='请求参数')
    rp_content = models.TextField(null=True, verbose_name='响应参数')
    rp_code = models.TextField(null=True, verbose_name='响应码')
    user_agent = models.TextField(null=True, verbose_name='请求浏览器')
    access_time = models.IntegerField(verbose_name='响应耗时/ms')

    class Meta:
        db_table = 'op_logs'
        verbose_name = '平台操作日志表'
        verbose_name_plural = '平台操作日志表'


class AccessTimeOutLogs(models.Model):
    '''超时操作日志表'''
    id = models.AutoField(primary_key=True)
    re_time = models.CharField(max_length=32, verbose_name='请求时间')
    re_user = models.CharField(max_length=32, verbose_name='操作人')
    re_ip = models.CharField(max_length=32, verbose_name='请求IP')
    re_url = models.CharField(max_length=255, verbose_name='请求url')
    re_method = models.CharField(max_length=11, verbose_name='请求方法')
    re_content = models.TextField(null=True, verbose_name='请求参数')
    rp_content = models.TextField(null=True, verbose_name='响应参数')
    rp_code = models.TextField(null=True, verbose_name='响应码')
    user_agent = models.TextField(null=True, verbose_name='请求浏览器')
    access_time = models.IntegerField(verbose_name='响应耗时/ms')

    class Meta:
        db_table = 'access_timeout_logs'
        verbose_name = '平台超时操作日志表'
        verbose_name_plural = '平台超时操作日志表'