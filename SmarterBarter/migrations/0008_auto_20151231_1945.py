# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-31 14:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmarterBarter', '0007_auto_20151230_0322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='currentRequests',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
