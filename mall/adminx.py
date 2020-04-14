import xadmin
from mall.models import Product


class ProductAdminx(object):
    # 商品信息后台管理
    list_display = ('name', 'type', 'price', 'is_valid')

    # 分页
    list_per_page = 10
    # 过滤器
    list_filter = ('type', 'status')

    # 按商品名称搜索
    search_fields = ('name',)


xadmin.site.register(Product, ProductAdminx)
