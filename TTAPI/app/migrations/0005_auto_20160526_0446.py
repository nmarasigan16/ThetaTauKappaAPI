# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-26 04:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20160518_2125'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chapter',
            options={'ordering': ['chapter_name']},
        ),
        migrations.AddField(
            model_name='meeting',
            name='attendance_taken',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='events',
            field=models.ManyToManyField(blank=True, to='app.Event'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='meetings',
            field=models.ManyToManyField(blank=True, to='app.Meeting'),
        ),
    ]
