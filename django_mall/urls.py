"""django_mall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django_mall import views, settings

import xadmin
from xadmin.plugins import xversion
xadmin.autodiscover()
xversion.register_models()


urlpatterns = [
    # dj自带的后台管理
    url(r'^admin/', admin.site.urls),

    # 自己安装的xadmin
    url(r'^xadmin/', xadmin.site.urls),

    # 首页
    url(r'^$', views.index, name='index'),

    # 商品模块url
    url(r'^mall/', include('mall.urls', namespace='mall')),

    # 系统模块url
    url(r'^sys/', include('system.urls', namespace='system')),

    # 用户模块url
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),

    # 个人中心模块url
    url(r'^m/', include('mine.urls', namespace='mine')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
