from django.contrib import admin

# Register your models here.
from mall.models import Product, Tag, Classify

# 注册的方式一
from utils.admin_actions import set_invalid, set_valid


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # 商品信息后台管理
    list_display = ('id','name', 'type', 'price', 'is_valid')
    # 自定义的方法配置
    actions = [set_invalid, set_valid]

    # 分页
    list_per_page = 10
    # 搜索
    list_filter = ('status',)


# 注册的方式二
# admin.site.register(Product,ProductAdmin)


@admin.register(Classify)
class ClassifyAdmin(admin.ModelAdmin):
    # 商品分类后台管理
    list_display = ['parent', 'name', 'code', 'is_valid']



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    # 商品分类后台管理
    list_display = [ 'name', 'code', 'is_valid']


