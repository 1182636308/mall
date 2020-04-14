from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db.models import F

from utils import constant


class User(AbstractUser):
    """用户基础信息表"""
    # username = models.CharField('用户名', max_length=64)
    # password = models.CharField('密码', max_length=255)
    nickname = models.CharField('昵称', max_length=64)
    avatar = models.ImageField('头像', upload_to='avatar', null=True, blank=True)
    integral = models.IntegerField('积分', default=10)
    level = models.SmallIntegerField('用户等级', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'accounts_user'
        verbose_name = '用户基础信息'
        verbose_name_plural = '用户基础信息'

    @property
    def default_addr(self):
        # 用户的默认的地址
        addr = None
        try:
            addr = self.user_address.filter(is_default=True, is_valid=True)[0]
        except IndexError:
            try:
                addr = self.user_address.filter(is_valid=True)[0]
            except IndexError:
                pass
        return addr

    @property
    def count_all(self):
        # 购物车上所有商品的总数量
        count = 0
        list = self.cart.filter(status=constant.ORDER_STATUS_INIT)
        for item in list:
            count += item.count
        return count

    def ope_integral_account(self, type, amount):
        # 积分的充值与消费
        # 充值
        if type == 1:
            self.integral = F('integral') + abs(amount)
            self.save()
            self.refresh_from_db()
        if type == 0:
            self.integral = F('integral') - abs(amount)
            self.save()
            self.refresh_from_db()


class UserProfile(models.Model):
    """用户详细信息表"""
    SEX_CHOICES = (
        (1, '男'), (0, '女')
    )
    user = models.OneToOneField(User)  # 一对一关联用户基础信息表
    real_name = models.CharField('真实姓名', max_length=64, )
    email = models.CharField('电子邮箱', max_length=128, null=True, blank=True)
    is_email_valid = models.BooleanField('邮箱是否验证', default=False)
    phone_no = models.CharField('手机号码', max_length=20, null=True, blank=True)
    is_phone = models.BooleanField('手机号码是否验证', default=False)
    sex = models.SmallIntegerField('性别', choices=SEX_CHOICES, default=1)
    age = models.SmallIntegerField('年龄', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    update_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        db_table = 'accounts_user_profile'
        verbose_name = '用户详细信息'
        verbose_name_plural = '用户详细信息'


class UserAddress(models.Model):
    """用户收货地址"""
    user = models.ForeignKey(User, related_name='user_address')
    province = models.CharField('省份', max_length=32)
    city = models.CharField('市区', max_length=32)
    area = models.CharField('区域', max_length=32)
    tomw = models.CharField('街道', max_length=32, null=True, blank=True)
    address = models.CharField('详情地址', max_length=128)
    obj = models.CharField('收件人', max_length=64)
    phone = models.CharField('收件人电话', max_length=32)
    is_valid = models.BooleanField('地址是否有效', default=True)
    is_default = models.BooleanField('是否为默认地址', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    update_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        db_table = 'accounts_user_address'
        ordering = ['is_default', '-created_at']
        verbose_name = '收货地址'
        verbose_name_plural = '收货地址'

    def get_phone_format(self):
        # 格式化手机号码，130xxxx0000
        return self.phone[0:3] + 'xxxx' + self.phone[7:]

    def get_regin_format(self):
        # 格式化省市区街道，广东省广州市天河区xxx街
        return '{self.province} {self.city} {self.area}'.format(self=self)

    def __str__(self):
        return self.get_regin_format() + self.address


class LoginRecord(models.Model):
    """用户登录历史记录"""
    user = models.ForeignKey(User)
    login_name = models.CharField('登录名', max_length=64)
    ip = models.CharField('登录IP', max_length=32)
    address = models.CharField('地址', max_length=32, null=True, blank=True)
    source = models.CharField('登录来源', max_length=32)
    created_at = models.DateTimeField('登录时间', auto_now_add=True)

    class Meta:
        db_table = 'accounts_login_record'


"""
class PasswdChangelog(models.Model):
    # 用户密码修改历史
    pass
"""
