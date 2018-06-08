# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-31 10:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openprofession', '0049_auto_20180531_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seminardata',
            name='sex',
            field=models.CharField(choices=[('away', 'заочно'), ('internally', 'очно'), ('internally_cert', 'участвую очно и хочу')], max_length=1, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='seminardata',
            name='type_of_participation',
            field=models.CharField(choices=[('m', 'мужской'), ('f', 'женский')], max_length=15, verbose_name='Пол'),
        ),
    ]
