# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-03-14 12:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='商品ID')),
                ('img', models.ImageField(upload_to='classify', verbose_name='主图')),
                ('name', models.CharField(max_length=12, verbose_name='名称')),
                ('code', models.CharField(blank=True, max_length=32, null=True, verbose_name='编码')),
                ('desc', models.CharField(blank=True, max_length=64, null=True, verbose_name='详情')),
                ('reorder', models.SmallIntegerField(default=0, verbose_name='排序')),
                ('is_valid', models.BooleanField(default=True, verbose_name='是否有效')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='mall.Classify')),
            ],
            options={
                'db_table': 'mall_classify',
                'ordering': ['-reorder'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='商品ID')),
                ('name', models.CharField(max_length=128, verbose_name='名称')),
                ('desc', models.CharField(blank=True, max_length=256, null=True, verbose_name='简单描述')),
                ('content', models.TextField(verbose_name='详情描述')),
                ('type', models.SmallIntegerField(choices=[(11, '实物商品'), (12, '虚拟商品')], default=11, verbose_name='商品类型')),
                ('price', models.FloatField(verbose_name='市场价格')),
                ('origin_price', models.FloatField(verbose_name='原价')),
                ('img', models.ImageField(upload_to='product', verbose_name='主图')),
                ('buy_link', models.CharField(blank=True, max_length=256, null=True, verbose_name='购买连接')),
                ('reorder', models.SmallIntegerField(default=0, verbose_name='排序')),
                ('status', models.SmallIntegerField(choices=[(11, '销售中'), (12, '已售罄'), (13, '已下架')], default=12, verbose_name='商品状态')),
                ('sku_count', models.IntegerField(default=0, verbose_name='库存')),
                ('ramain_count', models.IntegerField(default=0, verbose_name='剩余库存')),
                ('view_count', models.IntegerField(default=0, verbose_name='浏览次数')),
                ('score', models.FloatField(default=10.0, verbose_name='评分')),
                ('is_valid', models.BooleanField(default=True, verbose_name='是否有效')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('classes', models.ManyToManyField(related_name='classes', to='mall.Classify', verbose_name='分类')),
            ],
            options={
                'db_table': 'mall_product',
                'ordering': ['-reorder'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='标签ID')),
                ('img', models.ImageField(blank=True, null=True, upload_to='classify', verbose_name='主图')),
                ('name', models.CharField(max_length=12, verbose_name='名称')),
                ('code', models.CharField(blank=True, max_length=32, null=True, verbose_name='编码')),
                ('reorder', models.SmallIntegerField(default=0, verbose_name='排序')),
                ('is_valid', models.BooleanField(default=True, verbose_name='是否有效')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
            options={
                'db_table': 'mall_tag',
                'ordering': ['-reorder'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='tag',
            field=models.ManyToManyField(related_name='tag', to='mall.Tag', verbose_name='标签'),
        ),
    ]
