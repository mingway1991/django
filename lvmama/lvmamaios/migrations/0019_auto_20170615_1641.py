# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-15 16:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lvmamaios', '0018_consoleoutput'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consoleoutput',
            name='version',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='lvmamaios.Version'),
        ),
    ]
