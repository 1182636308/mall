from django.db.models import Q
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView

from accounts.models import UserAddress
from mall.models import Product
from mine.models import Collect
from utils import constant


def product_list(request):
    # 商品列表
    prod_list = Product.objects.filter(is_valid=True, status=constant.PRODUCT_STATUS_SELL)

    # 获取搜索返回的prod_name,在prod_list里筛选
    search_name = request.GET.get('search_name', '')
    if search_name:
        print(search_name)
        prod_list = prod_list.filter(name__icontains=search_name)

    return render(request, 'product_list.html', {
        'prod_list': prod_list
    })


def product_detail(request, uid):
    # 商品详情
    prod_obj = get_object_or_404(Product, uid=uid, is_valid=True)

    # 用户默认地址,购物车的物品数量
    user = request.user
    default_addr = None
    cart_count = 0
    if user.is_authenticated:
        default_addr = user.default_addr
        list = user.cart.filter(status=constant.ORDER_STATUS_INIT)
        for item in list:
            cart_count += item.count

    # 商品是否被用户收藏
    is_collect = None
    if user.is_authenticated:
        prod_collect = Collect.objects.get_or_create(user=user, product=prod_obj)[0]
        is_collect = prod_collect.is_collect
    return render(request, 'product_detail.html', {
        'prod_obj': prod_obj,
        'default_addr': default_addr,
        'cart_count':cart_count,
        'is_collect':is_collect
    })


class ProductList(ListView):
    # 商品列表
    # 每页放多少条数据
    model = Product
    paginate_by = 6
    # 模板位置
    template_name = 'product_list.html'

    def get_queryset(self):
        query = Q(is_valid=True, status=constant.PRODUCT_STATUS_SELL)

        # 获取搜索返回的prod_name,在prod_list里筛选
        search_name = self.request.GET.get('search_name', '')
        if search_name:
            query = query & Q(name__icontains=search_name)

        # tag标签进行分类筛选
        tag = self.request.GET.get('tag', '')
        if tag:
            query = query & Q(tag__code=tag)

        # 标签分类进行分类筛选
        cls = self.request.GET.get('cls', '')
        if cls:
            query = query & Q(classes__code=cls)

        return Product.objects.filter(query)

    def get_context_data(self, **kwargs):
        """添加变量到上下文"""
        context = super().get_context_data(**kwargs)
        context['context_data'] = self.request.GET.dict()
        return context


def product_classify(requset):
    # 商品分类页面的渲染
    return render(requset, 'classify.html', {
    })