# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-06 03:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0002_auto_20170506_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(db_index=True, max_length=100, primary_key=True, serialize=False),
        ),
    ]
