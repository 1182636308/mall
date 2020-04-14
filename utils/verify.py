"""
生成验证码：
1.准备素材，字体（ttf）,文字内容，干扰线，颜色
2.画验证码,创建图片
pip install Pillow
记录文字内容到cookie dj session机制
(1) 第一次请求,cookie[浏览器] + session[服务器] 对应关系生成
(2) 第二次请求,携带了cookie,找到对应的session[提交表单]

3.io文件流 BytesIO

"""
import os
import random
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse

from django_mall import settings


class VerifyCode(object):
    """验证码类"""

    def __init__(self, dj_request):
        self.dj_request = dj_request
        # 验证码尺寸
        self.img_wide = 100
        self.img_heigth = 30
        self.code_length = 4

        # 存入session的名称
        self.session_key = 'verify_code'

    def gen_code(self):
        # 生成验证码
        code = self._gen_code()
        # 把验证码存到session中
        self.dj_request.session[self.session_key] = code
        # 准备随机元素（文字颜色，背景颜色，干扰线）
        font_color = ['black', 'darkblue', 'darkred', 'brown', 'green', 'darkmagenta', 'red', 'pink', 'dimgray',
                      'forestgreen', 'darkviolet']
        # RGB随机背景色
        bg_color = (random.randrange(230, 255), random.randrange(230, 255), random.randrange(230, 255))
        # 字体路径
        font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'timesbi.ttf')

        # 创建图片
        im = Image.new('RGB', (self.img_wide, self.img_heigth), bg_color)
        draw = ImageDraw.Draw(im)
        # 添加干扰线,随机画1-2条
        for i in range(random.randrange(1, int(self.code_length / 2) + 1)):
            # 随机颜色，线宽，位置设置
            line_color = random.choice(font_color)
            width = random.randrange(1, 4)
            point = (
                random.randrange(0, self.img_wide * 0.2),
                random.randrange(0, self.img_heigth),
                random.randrange(self.img_wide - self.img_wide * 0.2, self.img_wide),
                random.randrange(0, self.img_heigth)
            )
            draw.line(point, fill=line_color, width=width)

        # 画验证码
        for index, char in enumerate(code):
            code_color = random.choice(font_color)
            font_size = random.randrange(16, 25)
            font = ImageFont.truetype(font_path, font_size)
            point = (index * self.img_wide / self.code_length,
                     random.randrange(0, self.img_heigth / 3))

            draw.text(point, char, fill=code_color, font=font)

        buf = BytesIO()
        im.save(buf, 'gif')
        return HttpResponse(buf.getvalue(), content_type='image/gif')

    def _gen_code(self):
        # 随机生成字符串
        random_str = 'QWERTYUOPASDFGHJKZXCVBNMqwertyuipasdfghjkzxcvbnm23456789'
        code_list = random.sample(random_str, self.code_length)
        code = ''.join(code_list)
        return code

    def validate_code(self, code):
        # 验证验证码是否正确
        # 大小写的转换
        code = str(code).lower()
        vcode = self.dj_request.session.get(self.session_key, '').lower()
        return code == vcode
