# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-19 07:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('openprofession', '0007_auto_20171218_1642'),
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024, verbose_name='Название программы(курса)')),
                ('active', models.BooleanField(default=False, verbose_name='Активна')),
                ('session', models.CharField(max_length=1024, verbose_name='Название сессии')),
            ],
        ),
        migrations.AddField(
            model_name='personaldata',
            name='all_docs',
            field=models.BooleanField(default=False, verbose_name='Слушатель прикрепил документы: скан заявления, документ об образовании'),
        ),
        migrations.AddField(
            model_name='personaldata',
            name='all_scans',
            field=models.BooleanField(default=False, verbose_name='Прикреплены все необоходимые сканы документов'),
        ),
        migrations.AddField(
            model_name='personaldata',
            name='all_valid',
            field=models.BooleanField(default=False, verbose_name='Данные в доках слушателя совпадают и корректны'),
        ),
        migrations.AddField(
            model_name='personaldata',
            name='city',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='personaldata',
            name='document_type',
            field=models.CharField(blank=True, choices=[('u', 'Удостоверение'), ('s', 'Сертификат'), ('n', 'Неуспеваемость')], max_length=1, null=True, verbose_name='Тип выдаваемого документа'),
        ),
        migrations.AddField(
            model_name='personaldata',
            name='in_quote',
            field=models.BooleanField(default=False, verbose_name='Попал в квоту'),
        ),
        migrations.AddField(
            model_name='personaldata',
            name='paid',
            field=models.BooleanField(default=False, verbose_name='Оплатил'),
        ),
        migrations.AddField(
            model_name='personaldata',
            name='quote',
            field=models.BooleanField(default=False, verbose_name='Заявка на попадание в квоту'),
        ),
        migrations.AddField(
            model_name='personaldata',
            name='status',
            field=models.CharField(blank=True, choices=[('f', 'Физ.лицо'), ('j', 'Физ.лицо по договору с юр.лицом')], max_length=1, null=True, verbose_name='Статус'),
        ),
        migrations.AddField(
            model_name='personaldata',
            name='program',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='openprofession.Program'),
        ),
    ]
