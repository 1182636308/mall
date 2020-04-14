from django.http import HttpResponse

from accounts.models import User


def ip_middleware(get_response):
    def middleware(request):
        # 请求到达之前的业务逻辑
        print('请求到达之前的业务逻辑')
        response = get_response(request)

        # IP被限制的业务
        ip = request.META.get('REMOTE_ADDR', None)
        print(ip)
        ip_disabled_list = [
            '127.0.0.1'
        ]
        if ip in ip_disabled_list:
            return HttpResponse('IP被限制', status=403)

        # 在视图函数调用之后的业务逻辑
        print('在视图函数调用之后的业务逻辑')
        return response

    return middleware


class MallAuthMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        # 请求到达之前的业务逻辑
        user_id = request.session.get('user_id', None)
        if user_id:
            user = User.objects.get(pk=user_id)
        else:
            user = None
        request.my_user = user
        response = self.get_response(request)

        # 在视图函数调用之后的业务逻辑
        print('在视图函数调用之后的业务逻辑')
        return response
