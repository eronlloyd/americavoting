# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-24 13:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20151222_2209'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='politicalparty',
            options={'verbose_name_plural': 'political parties'},
        ),
        migrations.AlterField(
            model_name='division',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 24, 8, 9, 18, 158726)),
        ),
    ]
