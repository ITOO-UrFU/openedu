# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-20 12:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openprofession', '0012_auto_20180120_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportentry',
            name='raw_data',
            field=models.TextField(default='', verbose_name='Raw'),
        ),
    ]
