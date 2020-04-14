from django.contrib import admin, messages

from django.contrib.auth.admin import UserAdmin
from accounts.models import User, UserProfile, UserAddress


@admin.register(User)
class UserAdmin(UserAdmin):
    # 用户后台管理
    list_display = ('format_username', 'nickname', 'integral', 'is_active')
    actions = ['disable_user', 'enable_user']

    def format_username(self, obj):
        # 用户名脱敏处理
        return obj.username[0:3] + '****'

    # 修改列名显示
    format_username.short_description = '用户名'

    # 按用户名和昵称搜索
    search_fields = ('username', 'nickname')

    def disable_user(self, request, queryset):
        # 自定义批量禁用用户的方法
        queryset.update(is_active=False)
        messages.success(request, '操作成功')

    disable_user.short_description = '批量禁用用户'

    def enable_user(self, request, queryset):
        # 自定义批量启用用户的方法
        queryset.update(is_active=True)
        messages.success(request, '操作成功')

    enable_user.short_description = '批量启用用户'

# 注册的方式二
# admin.site.register(User,UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # 用户详细信息后台管理
    list_display = ['user', 'real_name', 'email', 'is_email_valid', 'is_phone', 'sex', 'age']


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    # 用户收货地址后台管理
    list_display = ['user', 'obj', 'phone', 'province', 'city', 'area',
                    'tomw', 'address', 'is_valid', 'is_default']

    search_fields = ('user__username', 'obj')
