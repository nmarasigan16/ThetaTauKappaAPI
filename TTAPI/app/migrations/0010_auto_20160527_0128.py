# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-27 01:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_demographics_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brother',
            name='attendance_pass',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='brother',
            name='excuse',
            field=models.TextField(blank=True),
        ),
    ]
