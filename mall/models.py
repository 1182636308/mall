import uuid

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
from django.db.models import F

from accounts.models import User
from system.models import ImageFile
from utils import constant


class Classify(models.Model):
    """商品分类"""
    uid = models.UUIDField('商品ID', default=uuid.uuid4, editable=False)
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True)  # 自己外键关联自己
    img = models.ImageField('主图', upload_to='classify')
    name = models.CharField('名称', max_length=12)
    code = models.CharField('编码', max_length=32, null=True, blank=True)
    desc = models.CharField('详情', max_length=64, null=True, blank=True)
    reorder = models.SmallIntegerField('排序', default=0)
    is_valid = models.BooleanField('是否有效', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    update_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        db_table = 'mall_classify'
        ordering = ['-reorder']
        verbose_name = '商品分类'
        verbose_name_plural = '商品分类'

    def __str__(self):
        return '{0}-{1}'.format(self.code,self.name)



class Tag(models.Model):
    """商品的标签"""
    uid = models.UUIDField('标签ID', default=uuid.uuid4, editable=False)
    img = models.ImageField('主图', upload_to='classify', null=True, blank=True)
    name = models.CharField('名称', max_length=12)
    code = models.CharField('编码', max_length=32, null=True, blank=True)
    reorder = models.SmallIntegerField('排序', default=0)
    is_valid = models.BooleanField('是否有效', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    update_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        db_table = 'mall_tag'
        ordering = ['-reorder']
        verbose_name = '商品标签'
        verbose_name_plural = '商品标签'

    def __str__(self):
        return '{0}-{1}'.format(self.code,self.name)


class Product(models.Model):
    """商品信息"""
    # UUIDField 随机生成一串不重复的很长的字符串，editable=False不能编辑
    uid = models.UUIDField('商品ID', default=uuid.uuid4, editable=False)
    name = models.CharField('名称', max_length=128)
    desc = models.CharField('简单描述', max_length=256, null=True, blank=True)
    # content = models.TextField('详情描述')
    # 富文本
    content = RichTextField('详情描述')
    type = models.SmallIntegerField('商品类型',
                                    choices=constant.PRODUCT_TYPE_CHOICES,
                                    default=constant.PRODUCT_TYPE_ACTUAL)
    price = models.FloatField('市场价格')
    origin_price = models.FloatField('原价')
    img = models.ImageField('主图', upload_to='%Y%m/product')
    buy_link = models.CharField('购买连接', max_length=256, null=True, blank=True)
    reorder = models.SmallIntegerField('排序', default=0)
    status = models.SmallIntegerField('商品状态',
                                      choices=constant.PRODUCT_STATUS_CHOICES,
                                      default=constant.PRODUCT_STATUS_LOST)
    sku_count = models.IntegerField('库存', default=0)
    ramain_count = models.IntegerField('剩余库存', default=0)
    view_count = models.IntegerField('浏览次数', default=0)
    score = models.FloatField('评分', default=10.0)
    is_valid = models.BooleanField('是否有效', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    update_at = models.DateTimeField('修改时间', auto_now=True)
    tag = models.ManyToManyField(Tag, verbose_name='标签', related_name='tag')
    classes = models.ManyToManyField(Classify, verbose_name='分类', related_name='classes',null=True,blank=True)
    banners = GenericRelation(ImageFile, verbose_name='banner图', related_query_name='banners')


    class Meta:
        db_table = 'mall_product'
        ordering = ['-reorder']
        verbose_name = '商品信息'
        verbose_name_plural = '商品信息'


    def update_store_count(self,count):
        # 更新剩余库存数量
        self.ramain_count = F('ramain_count')-count
        self.save()
        self.refresh_from_db()


    def __str__(self):
        return '{0}'.format(self.name)


