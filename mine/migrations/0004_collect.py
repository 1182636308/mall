# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-03-28 08:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mall', '0005_auto_20200328_1658'),
        ('mine', '0003_auto_20200328_1652'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_collect', models.BooleanField(default=False, verbose_name='是否收藏')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mall.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '我的收藏',
                'verbose_name_plural': '我的收藏',
                'db_table': 'mine_collect',
                'ordering': ['-update_at'],
            },
        ),
    ]
