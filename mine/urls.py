from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from mine import views

urlpatterns = [
    # 个人中心
    url(r'^$', views.mine, name='mine'),

    # 订单管理
    url(r'^order/detail/(?P<sn>\S+)/$', login_required(views.OrderDetailView.as_view()), name='order_detail'),

    # 加入购物车
    url(r'^cart/add/(?P<prod_uid>\S+)/$', views.cart_add, name='cart_add'),

    # 我的购物车
    url(r'^cart/$', views.cart, name='cart'),

    # 积分支付
    url(r'^order/pay/$', views.order_pay, name='order_pay'),

    # 订单列表
    url(r'^order/list/$', login_required(views.OrderListView.as_view()), name='order_list'),

    # 我的收藏
    url(r'^prod/collect$', views.prod_collect, name='prod_collect'),

    # 将商品移除购物车
    url(r'^cart/del/(?P<prod_uid>\S+)/$', views.cart_del, name='cart_del'),

    # 添加收藏与删除收藏
    url(r'^prod/collect/move/(?P<prod_uid>\S+)/$', views.prod_collect_move, name='prod_collect_move'),

    # 确认收货
    url(r'^order/confirm/(?P<sn>\S+)/$', views.order_confirm, name='order_confirm'),

    # 删除订单
    url(r'^order/delete/(?P<sn>\S+)/$', views.order_delete, name='order_delete'),
]
