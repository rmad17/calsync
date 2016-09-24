# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-24 14:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='google_id',
            field=models.CharField(max_length=500, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='events',
            name='description',
            field=models.CharField(max_length=500),
        ),
    ]