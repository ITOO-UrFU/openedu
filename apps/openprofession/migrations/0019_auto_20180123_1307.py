# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-23 08:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openprofession', '0018_auto_20180123_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='personaldata',
            name='courses',
            field=models.ManyToManyField(related_name='personaldata_requests_created', to='openprofession.Program'),
        ),
        migrations.AddField(
            model_name='personaldata',
            name='entries',
            field=models.ManyToManyField(related_name='personaldata_requests_created', to='openprofession.ReportEntry'),
        ),
        migrations.AddField(
            model_name='personaldata',
            name='possible_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
