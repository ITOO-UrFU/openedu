# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-19 09:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openprofession', '0009_personaldata_another_doc'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuotesAvailable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available', models.BooleanField(default=False, verbose_name='Квота доступна')),
            ],
        ),
    ]
