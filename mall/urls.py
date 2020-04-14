from django.conf.urls import url

from mall import views

urlpatterns = [
    # 商品列表 使用def实现的
    # url(r'^product/list/$', views.product_list, name='product_list'),

    # 商品列表 使用class实现的
    url(r'^product/list/$', views.ProductList.as_view(), name='product_list'),

    # 加载商品列表中HTML片段的地址
    url(r'^product/load/list$', views.ProductList.as_view(
        template_name='product_load_list.html'
    ), name='product_load_list'),

    # 商品详情
    url(r'^product/detail/(?P<uid>\S+)/$', views.product_detail, name='product_detail'),

    # 商品分类页面
    url(r'^product/classify/$', views.product_classify, name='product_classify'),
]
