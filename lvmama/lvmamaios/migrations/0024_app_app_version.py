# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-16 11:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lvmamaios', '0023_app_module'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='app_version',
            field=models.CharField(default='', max_length=50),
        ),
    ]
