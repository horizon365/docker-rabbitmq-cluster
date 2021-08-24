# coding=utf-8
"""
权限管理数据库models
"""
from django.db import models
from django.utils import timezone
from django_jsonfield_backport.models import JSONField


class OperationLogs(models.Model):
    """
    OperationLogs models
    who, where, when, what, how
    """
    choices = (
        (True, '成功'),
        (False, '失败'),
    )

    id = models.BigIntegerField(primary_key=True)
    who_user = models.CharField(verbose_name='用户名称', max_length=50, blank=False, default='whomax')
    last_login = models.DateTimeField(verbose_name='最后一次登录时间')
    who_ip = models.GenericIPAddressField(verbose_name='登录ip', blank=False)
    when = models.DateTimeField(verbose_name='操作时间', default=timezone.localtime)
    how = models.CharField(verbose_name='动作', max_length=200)
    request_data = JSONField(verbose_name='请求的数据体', default=dict, null=True)
    what_before = JSONField(verbose_name='之前', default=dict, null=True)
    what_after = JSONField(verbose_name='之后', default=dict, null=True)
    where = models.CharField(max_length=50, blank=False)
    result = models.BooleanField(verbose_name='操作结果', blank=False, choices=choices)


class Role(models.Model):
    """
    角色表
    Role.user_set.all()
    todo : 使用-user这个多对多键的排序会导致queryset多个重复的管理员出现
    """
    name = models.CharField(verbose_name='组名称^^^^', max_length=50, unique=True, blank=False)
    description = models.TextField(blank=False)
    pages = JSONField(verbose_name='可访问页面')
    create_time = models.DateTimeField(verbose_name='创建时间', default=timezone.localtime)
    permission = models.TextField(blank=False, default='非管理员')

    class Meta:
        """
        重命名表名，设定排序
        """
        ordering = ['create_time']

    def __str__(self):
        return str(self.name)


class User(models.Model):
    """
    用户表
    """
    name = models.CharField(max_length=50, blank=False, unique=True)
    test = models.ForeignKey(OperationLogs, on_delete=models.CASCADE)
    role = models.ManyToManyField(Role)
    create_time = models.DateTimeField(verbose_name='创建时间', default=timezone.localtime)

    class Meta:
        """
        重命名表名，设定排序
        """
        ordering = ['create_time']

    def __str__(self):
        return str(self.name)
