from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

# Create your models here.
from accounts.models import User
from mall.models import Product
from system.models import ImageFile
from utils import constant


class Order(models.Model):
    """订单"""
    sn = models.CharField('订单编号', max_length=32)
    user = models.ForeignKey(User)
    buy_count = models.PositiveIntegerField('购买数量', default=1)
    buy_amount = models.FloatField('总额')
    # 快递信息
    to_user = models.CharField('收件人', max_length=32)
    to_area = models.CharField('省市区', max_length=32)
    to_address = models.CharField('详细地址', max_length=256)
    to_phone = models.CharField('电话', max_length=32)
    remark = models.CharField('备注', max_length=256, null=True, blank=True)
    express_type = models.CharField('快递公司', max_length=32, null=True, blank=True)
    express_no = models.CharField('快递单号', max_length=32, null=True, blank=True)
    status = models.SmallIntegerField('订单状态',
                                      choices=constant.ORDER_STATUS_CHOICES,
                                      default=constant.ORDER_STATUS_SUMBIT)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    update_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        db_table = 'mine_order'
        verbose_name = '订单管理'
        verbose_name_plural = '订单管理'

    def get_cart_product(self):
        # 购物车中已经下单的商品
        # 排除还在购物车状态的商品
        return self.cart.exclude(status=constant.ORDER_STATUS_INIT)

    def __str__(self):
        return self.sn


class Cart(models.Model):
    # 购物车
    user = models.ForeignKey(User,related_name='cart')
    product = models.ForeignKey(Product)
    order = models.ForeignKey(Order, null=True, blank=True,related_name='cart')
    # 商品快照
    name = models.CharField('商品名称', max_length=128)
    img = models.ImageField('主图', upload_to='order')
    price = models.FloatField('市场价')
    origin_price = models.FloatField('原价')
    count = models.PositiveIntegerField('购买数量', default=1)
    amount = models.FloatField('总额')
    status = models.SmallIntegerField('状态',
                                      choices=constant.ORDER_STATUS_CHOICES,
                                      default=constant.ORDER_STATUS_INIT)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    update_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        db_table = 'mine_cart'
        ordering = ['-created_at']
        verbose_name = '购物车'
        verbose_name_plural = '购物车'



class Comments(models.Model):
    # 商品评价
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    order = models.ForeignKey(Order)
    content = models.CharField('商品评价', max_length=256)
    reorder = models.SmallIntegerField('排序', default=0)
    is_anonymous = models.BooleanField('是否匿名', default=True)
    score = models.FloatField('商品评分', default=10.0)
    score_deliver = models.FloatField('配送服务', default=10.0)
    score_package = models.FloatField('快递包装', default=10.0)
    score_speed = models.FloatField('送货速度', default=10.0)
    img_list = GenericRelation(ImageFile, related_query_name='img_list', verbose_name='评价晒图')
    is_valid = models.BooleanField('是否有效', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    update_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        db_table = 'mine_product_comments'
        ordering = ['-reorder']
        verbose_name = '商品评价'
        verbose_name_plural = '商品评价'


class Collect(models.Model):
    # 我的收藏
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    is_collect = models.BooleanField('是否收藏',default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    update_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        db_table = 'mine_collect'
        ordering = ['-update_at']
        verbose_name = '我的收藏'
        verbose_name_plural = '我的收藏'