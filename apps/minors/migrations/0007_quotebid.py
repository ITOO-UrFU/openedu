# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-18 10:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minors', '0006_auto_20170911_1542'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuoteBid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=254, null=True, unique=True, verbose_name='Имя')),
                ('email', models.CharField(blank=True, max_length=254, null=True, unique=True, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=254, null=True, unique=True, verbose_name='Телефон')),
                ('course', models.CharField(blank=True, max_length=2048, null=True, verbose_name='Курс')),
                ('agreement', models.BooleanField(default=False, verbose_name='Согласие на обработку перс. данных')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('quoted', models.BooleanField(default=False, verbose_name='Попал в квоту')),
                ('done', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'заявка на квоту',
                'verbose_name_plural': 'заявки на квоту',
            },
        ),
    ]
