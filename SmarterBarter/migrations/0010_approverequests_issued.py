# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-02 05:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmarterBarter', '0009_approverequests'),
    ]

    operations = [
        migrations.AddField(
            model_name='approverequests',
            name='issued',
            field=models.IntegerField(default=0),
        ),
    ]
