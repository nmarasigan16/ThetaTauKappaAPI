# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-27 02:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20160527_0128'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='chapter',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app.Chapter'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='chapter',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app.Chapter'),
        ),
    ]
