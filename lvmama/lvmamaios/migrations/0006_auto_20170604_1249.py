# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-04 12:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lvmamaios', '0005_auto_20170602_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkstep',
            name='step_duration',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True),
        ),
    ]
