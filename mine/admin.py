from django.contrib import admin

# Register your models here.
from mine.models import Order, Cart, Comments, Collect


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # 订单后台管理
    list_display = ['sn', 'user', 'to_user', 'buy_count', 'buy_amount', 'to_phone', 'to_area',
                    'to_address', 'express_no', 'status']

    # 按用户名、昵称、收件人来查询
    search_fields = ['user__username', 'user__nickname', 'to_user']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    # 购物车后台管理
    list_display = ['user', 'product', 'order', 'name', 'price', 'count', 'status']


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    # 购物车后台管理
    list_display = ['product', 'user', 'order', 'content']


@admin.register(Collect)
class CommentsAdmin(admin.ModelAdmin):
    # 购物车后台管理
    list_display = ['product', 'user', 'is_collect', 'created_at', 'update_at']
