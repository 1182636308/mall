from django.conf.urls import url

from accounts import views

urlpatterns = [

    # 用户登录
    url(r'^user/login/$', views.user_login, name='user_login'),

    # 用户退出
    url(r'^user/logout/$', views.user_logout, name='user_logout'),

    # 用户注册
    url(r'^user/regist/$', views.user_regist, name='user_regist'),

    # 收货地址
    url(r'^user/address/list$', views.user_address_list, name='user_address_list'),

    # 新增或者修改收货地址 ,user/address/edit/add 与 user/address/edit/12
    url(r'^user/address/edit/(?P<pk>\S+)/$', views.user_address_edit, name='user_address_edit'),

    # 地址的删除
    url(r'^user/address/delete/(?P<pk>\d+)/$', views.user_address_delete, name='user_address_delete'),

    # 修改密码
    url(r'^change/pwd/$', views.change_pwd, name='change_pwd')
]
