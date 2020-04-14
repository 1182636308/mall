import re

from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password

from accounts.models import User, UserAddress
from utils.verify import VerifyCode


class UserLoginForm(forms.Form):
    # 用户登录表单
    username = forms.CharField(label='用户名', max_length=64, error_messages={
        'required': '请输入用户名'
    })
    password = forms.CharField(label='密码', widget=forms.PasswordInput, error_messages={
        'required': '请输入密码'
    })
    verify_code = forms.CharField(label='验证码', max_length=4, error_messages={
        'required': '请输入验证码'
    })

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    """
    # 单个字段验证的方法，函数名username必须是字段里有的
    def clean_username(self):
        # 验证用户名，hook,钩子函数
        username = self.cleaned_data['username']
        # print(username)
        pattern = r'^0{0,1}1\d{10}$'
        if not re.search(pattern, username):
            raise forms.ValidationError('请输入正确的手机号码')
        return username
    """

    def clean_verify_code(self):
        # 验证码的验证
        verify_code = self.cleaned_data['verify_code']
        if not verify_code:
            raise forms.ValidationError('请输入验证码')
        client = VerifyCode(self.request)
        if not client.validate_code(verify_code):
            raise forms.ValidationError('输入的验证码不正确')

    # 多个字段验证的方法，重写父类clean()
    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        # 获取用户名和密码，不建议使用[]的方式，而用get
        # username = cleaned_data['username']
        # 验证用户名是否存在
        username = cleaned_data.get('username', None)
        password = cleaned_data.get('password', None)
        user_list = User.objects.filter(username=username)
        if username and password:
            if user_list.count() == 0:
                raise forms.ValidationError('用户名不存在')
            # 验证密码是否正确
            if not authenticate(username=username, password=password):
                raise forms.ValidationError('密码不正确')
        return cleaned_data


class UserRegistForm(forms.Form):
    # 注册表单
    username = forms.CharField(label='用户名', max_length=64, error_messages={
        'required': '请输入手机号'
    })
    nickname = forms.CharField(label='昵称', max_length=64)
    password = forms.CharField(label='设置密码', widget=forms.PasswordInput)
    password_repeat = forms.CharField(label='确认密码', widget=forms.PasswordInput)
    verify_code = forms.CharField(label='验证码', max_length=4)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_username(self):
        # 验证用户名是否已经存在
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_verify_code(self):
        # 验证码的验证
        verify_code = self.cleaned_data['verify_code']
        if not verify_code:
            raise forms.ValidationError('请输入验证码')
        client = VerifyCode(self.request)

        if not client.validate_code(verify_code):
            raise forms.ValidationError('输入的验证码不正确')
        return verify_code

    def clean(self):
        # 验证两次输入的密码是否一致
        cleaned_data = super().clean()
        password = cleaned_data.get('password', None)
        password_repeat = cleaned_data.get('password_repeat', None)
        if password and password_repeat:
            if password != password_repeat:
                raise forms.ValidationError('两次输入的密码不一致')
        return cleaned_data

    def register(self):
        # 创建用户
        data = self.cleaned_data
        User.objects.create_user(username=data['username'],
                                 password=data['password'],
                                 nickname=data['nickname'])
        # 自动登录
        user = authenticate(username=data['username'], password=data['password'])
        login(self.request, user)
        return user


class UserAddressEdit(forms.ModelForm):
    # 用户收货地址表单
    region = forms.CharField(label='大区域选项', max_length=64, required=True, error_messages={
        'required': '请选择地址'
    })

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    class Meta:
        model = UserAddress
        fields = ['address', 'obj', 'phone', 'is_default']
        widgets = {
            'is_default': forms.CheckboxInput(attrs={
                'class': ' weui-switch'
            })
        }

    def clean_phone(self):
        # 验证手机号
        phone = self.cleaned_data['phone']
        pattern = r'^1\d{10}$'
        if not re.search(pattern, phone):
            raise forms.ValidationError('请输入正确的手机号码')
        return phone

    def clean(self):
        # 验证收货地址是否大于20条
        cleaned_data = super().clean()
        # 查询档期用户收货地址的信息
        address_list = UserAddress.objects.filter(is_valid=True, user=self.request.user)
        if address_list.count() > 20:
            raise forms.ValidationError('最多保存20个地址')
        return cleaned_data

    def save(self, commit=True):
        mod_obj = super().save(commit=False)
        region = self.cleaned_data['region']
        (province, city, area) = region.split(' ')
        mod_obj.province = province
        mod_obj.city = city
        mod_obj.area = area
        mod_obj.user = self.request.user

        # 有默认地址，当前表单勾选了默认地址，需要把之前那些默认的改为非默认的
        if self.cleaned_data['is_default']:
            user_addr = UserAddress.objects.filter(is_valid=True,
                                                   user=self.request.user,
                                                   is_default=True)
            user_addr.update(is_default=False)
        mod_obj.save()
        return mod_obj


class ChangePassword(forms.Form):
    # 修改密码
    old_password = forms.CharField(label='原密码', max_length=64, error_messages={
        'required': '请输入原密码'
    })
    new_password = forms.CharField(label='新密码', max_length=64, error_messages={
        'required': '请输入新密码'
    })
    new_password_repeat = forms.CharField(label='重复密码', max_length=64, error_messages={
        'required': '请输入新密码'
    })
    verify_code = forms.CharField(label='验证码', max_length=6, error_messages={
        'required': '请输入验证码'
    })

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_old_password(self):
        # 验证原密码是否正确
        old_password = self.cleaned_data['old_password']
        user = self.request.user
        # check_password(明文，密文)
        if not check_password(old_password, user.password):
            raise forms.ValidationError('原密码错误')
        return old_password

    def clean_verify_code(self):
        # 验证验证码是否输入正确
        verify_code = self.cleaned_data['verify_code']
        client = VerifyCode(self.request)
        if not client.validate_code(verify_code):
            raise forms.ValidationError('输入的验证码不正确')
        return verify_code

    def clean(self):
        # 判断两次输入的密码是否一致
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password', None)
        new_password_repeat = cleaned_data.get('new_password_repeat', None)
        if new_password != new_password_repeat:
            raise forms.ValidationError('两次输入的密码不一致')
        return cleaned_data
