# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-12 15:04
from __future__ import unicode_literals

from django.db import migrations, models
import elearning.models


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0007_auto_20170512_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='material_file',
            field=models.FileField(default='s', upload_to=elearning.models.get_file_path),
            preserve_default=False,
        ),
    ]
