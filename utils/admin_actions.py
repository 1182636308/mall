"""后台添加的自定义方法，公用部分"""
from django.contrib import messages


def set_invalid(modeladmin, request, queryset):
    # 批量禁用
    queryset.update(is_valid=False)
    messages.success(request, '操作成功')


set_invalid.short_description = '批量禁用所选对象'


def set_valid(modeladmin, request, queryset):
    # 批量启用
    queryset.update(is_valid=True)
    messages.success(request, '操作成功')


set_valid.short_description = '批量启用所选对象'
