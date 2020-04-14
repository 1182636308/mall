from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import render, get_object_or_404

# Create your views here.
from system.models import News
from utils import constant
from utils.verify import VerifyCode


def news_list(request):
    # 新闻列表
    news = News.objects.filter(type=constant.NEWS_TYPE_NEW,
                               is_valid=True)
    page_size = 20  # 一页显示20条数据
    page = request.GET.get('page', default=1)
    paginator_obj = Paginator(news, page_size)
    page_data = paginator_obj.page(page)
    return render(request, 'news_list.html', {
        'news_list': news,
        'page_data': page_data,
    })


def news_detail(request, pk):
    # 新闻详情
    # 如果查询不到就返回404
    news_obj = get_object_or_404(News, pk=pk, is_valid=True)
    # 每查看一次。浏览次数加1，使用F函数在数据库层面操作数据，防止并发产生数据的错误
    news_obj.view_count = F('view_count') + 1
    news_obj.save()
    # 重新从数据库取数据
    news_obj.refresh_from_db()
    return render(request, 'news_info.html', {
        'news_obj': news_obj
    })


def verify_code(request):
    # 验证码的生成
    client = VerifyCode(request)
    return client.gen_code()
