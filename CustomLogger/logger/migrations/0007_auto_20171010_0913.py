# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-10 09:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0006_auto_20171007_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logentry',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
