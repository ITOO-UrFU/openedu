# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-25 09:30
from __future__ import unicode_literals

from django.db import migrations, models
import openprofession.models


class Migration(migrations.Migration):

    dependencies = [
        ('openprofession', '0029_auto_20180125_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personaldata',
            name='diploma_scan',
            field=models.FileField(default='sdf', upload_to=openprofession.models.generate_new_filename, verbose_name='Скан диплома'),
            preserve_default=False,
        ),
    ]
