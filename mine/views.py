from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q, Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction

# Create your views here.
from django.views.generic import DetailView, ListView

from mall.models import Product
from mine.models import Order, Cart, Collect
from utils import constant
from utils.tools import gen_trans_id


def mine(requset):
    # 个人中心
    # 订单类型的数量
    sumbit_count, paied_count, sent_count, done_count = 0, 0, 0, 0
    try:
        order_list = Order.objects.filter(user=requset.user)
        for order in order_list:
            if order.status == constant.ORDER_STATUS_SUMBIT:
                sumbit_count += 1
            elif order.status == constant.ORDER_STATUS_PAIED:
                paied_count += 1
            elif order.status == constant.ORDER_STATUS_SENT:
                sent_count += 1
            elif order.status == constant.ORDER_STATUS_DONE:
                done_count += 1
    except:
        pass

    return render(requset, 'mine.html', {
        'constant': constant,
        'sumbit_count': sumbit_count,
        'paied_count': paied_count,
        'sent_count': sent_count,
        'done_count': done_count
    })


class OrderDetailView(DetailView):
    # 订单详情
    model = Order
    template_name = 'order_info2.html'
    slug_field = 'sn'
    slug_url_kwarg = 'sn'

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content['constant'] = constant
        return content


@login_required
@transaction.atomic()
def cart_add(request, prod_uid):
    user = request.user
    # 将商品加入购物车
    product = get_object_or_404(Product,
                                uid=prod_uid, is_valid=True,
                                status=constant.PRODUCT_STATUS_SELL)
    # 从页面获取购买数量
    count = int(request.POST.get('count', 1))

    # 库存校验
    if product.ramain_count < count:
        print(product.ramain_count)
        return HttpResponse('no')
    # 减库存
    product.update_store_count(count)
    # 生成购物车记录
    try:
        cart = Cart.objects.get(product=product, user=user, status=constant.ORDER_STATUS_INIT)
        cart.count += count
        cart.amount = cart.count * cart.price
        cart.save()
    except Cart.DoesNotExist:
        Cart.objects.create(
            user=user,
            product=product,
            name=product.name,
            img=product.img,
            price=product.price,
            origin_price=product.origin_price,
            count=count,
            amount=count * product.price
        )
    return HttpResponse('ok')


@login_required
@transaction.atomic()
def cart(request):
    # 我的购物车
    user = request.user
    cart_list = user.cart.filter(status=constant.ORDER_STATUS_INIT)
    # 总金额
    sum_amunt = cart_list.aggregate(sum_amunt=Sum('amount'))

    if request.method == 'POST':
        # 保存用户地址
        # 修改购物车状态，生成订单
        default_addr = user.default_addr
        if not default_addr:
            messages.warning(request, '请添加地址信息')
            return redirect('accounts:user_address_list')
        # 计算商品总数量，与总价
        cart_total = cart_list.aggregate(sum_count=Sum('count'), sum_amount=Sum('amount'))
        order = Order.objects.create(
            sn=gen_trans_id(),
            user=user,
            buy_count=cart_total['sum_count'],
            buy_amount=cart_total['sum_amount'],
            to_user=default_addr.obj,
            to_area=default_addr.get_regin_format(),
            to_address=default_addr.address,
            to_phone=default_addr.phone
        )
        cart_list.update(
            status=constant.ORDER_STATUS_SUMBIT,
            order=order
        )
        # 跳转到订单详情，并消息通知
        messages.success(request, '下单成功，请支付')
        return redirect('mine:order_detail', order.sn)
    return render(request, 'shopcart.html', {
        'cart_list': cart_list,
        'sum_amunt': sum_amunt['sum_amunt']
    })


@login_required
@transaction.atomic()
def order_pay(request):
    # 积分支付
    user = request.user
    if request.method == 'POST':
        sn = request.POST.get('sn', None)
        # 查询订单信息
        order = get_object_or_404(Order, user=user, sn=sn)
        # 验证积分是否足够
        if order.buy_amount > user.integral:
            messages.error(request, '积分余额不足')
            return redirect('mine:order_detail', sn=sn)
        # 扣除积分,订单状态改为已付款
        user.ope_integral_account(0, order.buy_amount)
        order.status = constant.ORDER_STATUS_PAIED
        order.save()
        # 修改购物车中的状态
        order.cart.all().update(status=constant.ORDER_STATUS_PAIED)
        messages.success(request, '支付成功')
    return redirect('mine:order_detail', sn=sn)


@login_required
def order_list(request):
    # 订单列表
    status = request.GET.get('status', '')
    if status:
        try:
            status = int(status)
        except ValueError:
            status = ''
    return render(request, 'order_list.html', {
        'constant': constant,
        'status': status
    })


class OrderListView(ListView):
    # 用面向对象的方式形成订单列表
    model = Order
    template_name = 'order_list.html'

    def get_queryset(self):
        status = self.request.GET.get('status', '')

        user = self.request.user
        query = Q(user=user)
        if status:
            query = query & Q(status=status)
        return Order.objects.filter(query).exclude(
            status=constant.ORDER_STATUS_DELETE
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['constant'] = constant
        status = self.request.GET.get('status', '')
        if status:
            try:
                status = int(status)
            except ValueError:
                status = ''
        context['status'] = status
        return context


@login_required
def prod_collect(request):
    # 我的收藏
    user = request.user
    collect_list = Collect.objects.filter(user=user, is_collect=True)

    return render(request, 'prod_collect.html', {
        'collect_list': collect_list
    })


@login_required
def cart_del(request, prod_uid):
    # 将商品移除购物车
    # 获取在状态在购物车的列表
    product = get_object_or_404(Product, uid=prod_uid)
    cart_list = Cart.objects.filter(status=constant.ORDER_STATUS_INIT, product=product)
    # 删除状态在购物车的商品
    # 回减库存
    count = int(request.GET.get('count'))
    product.update_store_count(-count)
    cart_list.delete()
    return HttpResponse('OK')


@login_required
def prod_collect_move(request, prod_uid):
    # 添加收藏与删除收藏
    product = get_object_or_404(Product, uid=prod_uid, is_valid=True)
    user = request.user
    # 如果没有收藏记录就默认添加一条
    prod_collect = Collect.objects.get_or_create(user=user, product=product)[0]
    if prod_collect.is_collect:
        prod_collect.is_collect = False
        prod_collect.save()
    else:
        prod_collect.is_collect = True
        prod_collect.save()
    return HttpResponse('ok')


@login_required
def order_confirm(request, sn):
    # 确认收货
    # 获取订单对象，修改订单状态为以完成
    order_obj = get_object_or_404(Order, sn=sn, status=constant.ORDER_STATUS_SENT)
    if order_obj:
        order_obj.status = constant.ORDER_STATUS_DONE
        order_obj.save()
    else:
        return HttpResponse('no')
    return HttpResponse('ok')


@login_required
def order_delete(request, sn):
    # 删除订单
    # 获取订单对象，修改订单状态为删除
    order_obj = get_object_or_404(Order, sn=sn, status=constant.ORDER_STATUS_SUMBIT)
    if order_obj:
        order_obj.status = constant.ORDER_STATUS_DELETE
        order_obj.save()
    else:
        return HttpResponse('no')
    return HttpResponse('ok')
