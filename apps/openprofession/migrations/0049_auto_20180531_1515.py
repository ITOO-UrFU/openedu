# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-31 10:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openprofession', '0048_auto_20180531_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='seminardata',
            name='sex',
            field=models.CharField(blank=True, choices=[('away', 'заочно'), ('internally', 'очно'), ('internally_cert', 'участвую очно и хочу')], max_length=1, null=True, verbose_name='Пол'),
        ),
        migrations.AddField(
            model_name='seminardata',
            name='type_of_participation',
            field=models.CharField(blank=True, choices=[('m', 'мужской'), ('f', 'женский')], max_length=15, null=True, verbose_name='Пол'),
        ),
    ]
