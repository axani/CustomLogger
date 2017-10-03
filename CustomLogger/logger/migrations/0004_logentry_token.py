# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 18:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tokenizer', '0001_initial'),
        ('logger', '0003_logentry'),
    ]

    operations = [
        migrations.AddField(
            model_name='logentry',
            name='token',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='tokenizer.Token'),
            preserve_default=False,
        ),
    ]