# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-26 07:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openprofession', '0033_auto_20180126_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='personaldata',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='personaldata',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
