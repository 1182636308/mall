# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-03-21 08:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200318_2248'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '用户基础信息', 'verbose_name_plural': '用户基础信息'},
        ),
    ]
