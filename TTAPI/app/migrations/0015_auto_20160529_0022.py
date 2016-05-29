# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-29 00:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20160528_2122'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='name',
            field=models.CharField(default='Happy Hour', max_length=30),
        ),
        migrations.AlterField(
            model_name='event',
            name='etype',
            field=models.CharField(choices=[('PR', 'Professional'), ('BR', 'Brotherhood'), ('PH', 'Philanthropy')], default='BR', max_length=2),
        ),
    ]