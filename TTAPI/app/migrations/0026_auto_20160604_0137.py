# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-04 01:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_auto_20160604_0022'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='attendance', serialize=False, to='app.UserProfile')),
                ('password', models.CharField(blank=True, max_length=50)),
                ('excuse', models.TextField(blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='brother',
            name='attendance_pass',
        ),
        migrations.RemoveField(
            model_name='brother',
            name='excuse',
        ),
    ]
