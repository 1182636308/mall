from datetime import datetime
import logging
from django.shortcuts import render

from accounts.models import User
from mall.models import Product, Classify
from system.models import Slider, News
from utils import constant

logger = logging.getLogger('django')


def index(request):
    """首页"""
    # print('request.my_user:', request.my_user)
    # logger.debug('调试信息')
    # logger.warning('警告信息')
    # logger.error('错误信息')

    # 查询轮播图
    slider_list = Slider.objects.filter(position=constant.SLIDER_POSI_INDEX)

    # 首页的新闻,置顶，有效的，且在生效日期内的
    now_time = datetime.now()
    news_list = News.objects.filter(
        type=constant.NEWS_TYPE_NEW,
        is_top=True,
        is_valid=True,
        start_time__lt=now_time,
        end_time__gt=now_time,
    )
    # 登录的方式一
    # 从session中获取用户ID
    # user_id = request.session[constant.LOGIN_SESSION_ID]
    # 根据用户信息查询用户信息
    # user = User.objects.get(id=user_id)

    # 商品精选精选推荐、酒水推荐、猜你喜欢
    jx_prod = Product.objects.filter(
        status=constant.PRODUCT_STATUS_SELL,
        is_valid=True,
        tag__code='jx'
    )
    js_prod = Product.objects.filter(
        status=constant.PRODUCT_STATUS_SELL,
        is_valid=True,
        tag__code='js'
    )
    cn_prod = Product.objects.filter(
        status=constant.PRODUCT_STATUS_SELL,
        is_valid=True,
        tag__code='cn'
    )

    # 酒水专场分类
    classify = Classify.objects.filter(code='jszc')[0]

    return render(request, 'index.html', {
        'slider_list': slider_list,
        'news_list': news_list,
        # 'user':user
        'jx_prod': jx_prod,
        'js_prod': js_prod,
        'cn_prod': cn_prod,
        'classify': classify
    })
