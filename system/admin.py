from django.contrib import admin

# Register your models here.
from system.models import News, Slider, ImageFile
from utils.admin_actions import set_invalid, set_valid


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'is_valid')
    actions = [set_invalid, set_valid]


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    # 轮播图后台管理
    list_display = ('name', 'start_time', 'end_time', 'is_valid')
    actions = [set_invalid, set_valid]


@admin.register(ImageFile)
class ImageFileAdmin(admin.ModelAdmin):
    # 图片后台管理
    list_display = ['summary', 'img', 'content_obj', 'is_valid']


