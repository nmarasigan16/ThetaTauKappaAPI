# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-18 03:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20160518_0331'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='uid',
            new_name='id',
        ),
    ]