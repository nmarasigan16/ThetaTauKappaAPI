# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-31 06:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20160531_0038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
    ]
