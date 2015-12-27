# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-27 13:34
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20151227_0832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='upload_date',
            field=models.DateField(default=datetime.datetime(2015, 12, 27, 13, 34, 8, 23457, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='division',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 27, 13, 34, 8, 21930, tzinfo=utc)),
        ),
    ]
