# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-24 11:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openprofession', '0024_auto_20180124_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='reports',
            field=models.ManyToManyField(blank=True, to='openprofession.Report'),
        ),
    ]
