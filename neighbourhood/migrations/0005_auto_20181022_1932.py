# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-22 16:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neighbourhood', '0004_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='Text',
            field=models.CharField(max_length=250),
        ),
    ]
