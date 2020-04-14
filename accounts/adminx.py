import xadmin
from accounts.models import UserAddress


class UserAddressAdminx(object):
    # 商品信息后台管理
    list_display = ('user', 'address', 'obj', 'phone', 'is_valid')

    # 分页
    list_per_page = 10

    # 按用户名，收件人名称搜索
    search_fields = ('user','obj')


xadmin.site.register(UserAddress, UserAddressAdminx)
