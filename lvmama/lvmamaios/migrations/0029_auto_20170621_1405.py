# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-21 14:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lvmamaios', '0028_moduleversion_is_success'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moduleversion',
            name='is_success',
            field=models.BooleanField(default=False),
        ),
    ]