# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-28 03:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20160527_0252'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hours',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.UserProfile')),
                ('brotherhood', models.FloatField(default=0)),
                ('philanthropy', models.FloatField(default=0)),
                ('professional', models.FloatField(default=0)),
            ],
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['date']},
        ),
        migrations.RemoveField(
            model_name='brother',
            name='brotherhood',
        ),
        migrations.RemoveField(
            model_name='brother',
            name='philanthropy',
        ),
        migrations.RemoveField(
            model_name='brother',
            name='professional',
        ),
        migrations.RemoveField(
            model_name='pledge',
            name='philanthropy',
        ),
        migrations.RemoveField(
            model_name='pledge',
            name='professional',
        ),
        migrations.RemoveField(
            model_name='pledge',
            name='social',
        ),
        migrations.AddField(
            model_name='event',
            name='duration',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='etype',
            field=models.CharField(choices=[('PR', 'Professional'), ('BR', 'Brotherhood'), ('PH', 'Philanthropy')], default='PR', max_length=2),
        ),
    ]