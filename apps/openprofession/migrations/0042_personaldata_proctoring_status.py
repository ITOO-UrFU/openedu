# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-09 09:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openprofession', '0041_auto_20180407_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='personaldata',
            name='proctoring_status',
            field=models.CharField(blank=True, default='one', max_length=32, null=True, verbose_name='Статус прокторинга за выбранный курс'),
        ),
    ]
