# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-03-28 08:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mall', '0004_collect'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collect',
            name='product',
        ),
        migrations.RemoveField(
            model_name='collect',
            name='user',
        ),
        migrations.DeleteModel(
            name='Collect',
        ),
    ]
