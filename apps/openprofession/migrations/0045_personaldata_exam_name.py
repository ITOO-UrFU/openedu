# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-09 13:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openprofession', '0044_personaldata_exam_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='personaldata',
            name='exam_name',
            field=models.CharField(blank=True, default='', max_length=32, null=True, verbose_name='Название итогового мероприятия'),
        ),
    ]
