# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-03-22 08:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0003_auto_20200321_1634'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imagefile',
            options={'verbose_name': '图片', 'verbose_name_plural': '图片'},
        ),
        migrations.AlterField(
            model_name='imagefile',
            name='is_valid',
            field=models.BooleanField(default=True, verbose_name='是否有效'),
        ),
    ]
