from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout

from accounts.forms import UserLoginForm, UserRegistForm, UserAddressEdit, ChangePassword
from accounts.models import UserAddress

from utils import constant
from utils.verify import VerifyCode


def user_login(request):
    # 用户登录表单
    # 第一次输入URL,GET展示表单,仅供用户输入
    # 第二次输入URL,POST
    # 如果是从其他地方跳转到登录页面，则取next_url，登录后直接到其他地方的页面
    next_url = request.GET.get('next', 'index')

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST, request=request)
        # 验证表单数据是否合法
        if form.is_valid():
            """登录的方式一：
            # 登录后取表单数据
            data = form.cleaned_data
            # 查询用户
            user = User.objects.get(username=data['username'],password=data['password'])
            # 将用户id放到 session里
            request.session[constant.LOGIN_SESSION_ID] = user.id
            print('数据合法验证通过')
            """
            # 使用django-outh来登录
            data = form.cleaned_data
            # 验证是否通过，然后登录
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                request.session['user_id'] = user.id
            # 登录后跳转
            messages.success(request, '登录成功')
            return redirect(next_url)
        else:
            print(form.errors)
    else:
        form = UserLoginForm(request=request)
    return render(request, 'login.html', {
        'form': form,
        'next_url': next_url
    })


@login_required
def user_logout(request):
    # 用户退出登录
    logout(request)
    return redirect('index')


def user_regist(request):
    # 用户注册
    if request.method == 'POST':
        form = UserRegistForm(request, data=request.POST)
        if form.is_valid():
            # 验证通过后调用注册方法，并跳转到首页
            form.register()
            messages.success(request, '用户注册成功，并自动登录')
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = UserRegistForm(request)

    return render(request, 'regist.html', {
        'form': form
    })


@login_required
def user_address_list(request):
    # 收货地址
    address_list = UserAddress.objects.filter(user=request.user, is_valid=True)

    return render(request, 'address_list.html', {
        'address_list': address_list
    })


@login_required
def user_address_edit(request, pk):
    # 新增或者修改收货地址
    # 如果PK是数字表示修改
    user = request.user
    addr = None
    initial = {}
    if pk.isdigit():
        # 是数字
        addr = get_object_or_404(UserAddress, pk=pk, user=user, is_valid=True)
        initial['region'] = addr.get_regin_format()

    if request.method == 'POST':
        form = UserAddressEdit(request=request, data=request.POST,
                               instance=addr, initial=initial)
        if form.is_valid():
            form.save()
            return redirect('accounts:user_address_list')
        else:
            print(form.errors)
    else:
        form = UserAddressEdit(request=request, instance=addr, initial=initial)
    return render(request, 'address_edit.html', {
        'form': form,
        'pk': pk
    })


@login_required
def user_address_delete(request, pk):
    # 删除收货地址
    addr = get_object_or_404(UserAddress, user=request.user, pk=pk, is_valid=True)
    addr.is_valid = False
    addr.save()
    return HttpResponse('ok')


@login_required
def change_pwd(request):
    # 修改密码
    if request.method == 'POST':
        form = ChangePassword(request=request, data=request.POST)
        if form.is_valid():
            # 表单验证成功后，修改数据库数据
            user = request.user
            # make_password加密
            new_password = make_password(request.POST['new_password'])
            user.password = new_password
            user.save()
            # 修改成功后，消息提示，并跳转到首页
            messages.success(request, '密码修改成功,请重新登录')
            return redirect('accounts:user_login')
        else:
            print(form.errors)
    else:
        form = ChangePassword(request=request)

    return render(request, 'pwd_change.html', {
        'form': form
    })
