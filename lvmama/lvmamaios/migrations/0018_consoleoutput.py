# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-15 10:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lvmamaios', '0017_auto_20170614_1321'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsoleOutput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('console_start_user', models.CharField(default='', max_length=50)),
                ('console_message', models.TextField()),
                ('console_start_date', models.DateTimeField(null=True)),
                ('console_end_date', models.DateTimeField(null=True)),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lvmamaios.Version')),
            ],
        ),
    ]
