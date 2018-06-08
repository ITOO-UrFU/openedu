# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-01 05:38
from __future__ import unicode_literals

from django.db import migrations, models
import openprofession.models


class Migration(migrations.Migration):

    dependencies = [
        ('openprofession', '0050_auto_20180531_1516'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='seminardata',
            options={'verbose_name': 'участник семинара', 'verbose_name_plural': 'участники семинара'},
        ),
        migrations.AddField(
            model_name='seminardata',
            name='agreement',
            field=models.BooleanField(default=False, verbose_name='Согласие на обработку перс. данных'),
        ),
        migrations.AlterField(
            model_name='seminardata',
            name='another_doc',
            field=models.FileField(blank=True, null=True, upload_to=openprofession.models.generate_new_seminar_filename, verbose_name='Документ о смене персональных данных'),
        ),
        migrations.AlterField(
            model_name='seminardata',
            name='diploma_scan',
            field=models.FileField(blank=True, null=True, upload_to=openprofession.models.generate_new_seminar_filename, verbose_name='Cкан документа о базовом образовании'),
        ),
        migrations.AlterField(
            model_name='seminardata',
            name='education_bid',
            field=models.FileField(blank=True, null=True, upload_to=openprofession.models.generate_new_seminar_filename, verbose_name='Скан заявления о зачислении на обучение'),
        ),
        migrations.AlterField(
            model_name='seminardata',
            name='sex',
            field=models.CharField(choices=[('m', 'мужской'), ('f', 'женский')], max_length=1, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='seminardata',
            name='type_of_participation',
            field=models.CharField(choices=[('away', 'заочно'), ('internally', 'очно')], max_length=15, verbose_name='Тип участия'),
        ),
    ]
