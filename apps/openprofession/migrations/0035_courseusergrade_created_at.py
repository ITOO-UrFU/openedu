# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-27 13:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openprofession', '0034_auto_20180126_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseusergrade',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
