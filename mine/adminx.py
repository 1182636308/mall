import xadmin
from mine.models import Order


class OrderAdminx(object):
    # 商品信息后台管理
    list_display = ['user', 'to_user', 'buy_count', 'buy_amount', 'to_phone', 'to_area',
                    'to_address', 'express_no', 'status']

    # 分页
    list_per_page = 10

    # 按用户名，收件人名称搜索
    search_fields = ('user__username', 'to_user')



xadmin.site.register(Order, OrderAdminx)
