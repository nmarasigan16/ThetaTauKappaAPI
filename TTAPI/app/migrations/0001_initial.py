# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-18 03:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('chapter_id', models.AutoField(primary_key=True, serialize=False)),
                ('chapter_name', models.CharField(choices=[('K', 'Kappa')], default='K', max_length=2)),
                ('university', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('event_id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('location', models.TextField()),
                ('about', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('meeting_id', models.AutoField(primary_key=True, serialize=False)),
                ('mtype', models.CharField(choices=[('PM', 'Pledge Meeting'), ('GM', 'General Meeting'), ('VO', 'Voting'), ('IN', 'Initiation')], default='GM', max_length=2)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('year', models.CharField(choices=[('FR', 'Freshman'), ('SO', 'Sophomore'), ('JR', 'Junior'), ('SR', 'Senior'), ('AL', 'Alum')], default='FR', max_length=2)),
                ('major', models.CharField(choices=[('AE', 'Aerospace Engineering'), ('AB', 'Agricultural and Biological Engineering'), ('BE', 'Bioengineering'), ('CH', 'Chemical Engineering'), ('CE', 'Civil Engineering'), ('CO', 'Computer Engineering'), ('CS', 'Computer Science'), ('EE', 'Electrical Engineering'), ('GE', 'General Engineering'), ('IE', 'Industrial Engineering'), ('MA', 'Materials Science and Engineering'), ('ME', 'Mechanical Engineering/Engineering Mechanics'), ('NE', 'Nuclear, Plasma, and Radiological Engineering'), ('UE', 'Undeclared Engineering')], default='UE', max_length=2)),
                ('status', models.CharField(choices=[('P', 'Pledge'), ('B', 'Brother'), ('A', 'Alumni')], default='B', max_length=1)),
                ('officer', models.BooleanField(default=False)),
                ('create_date', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['chapter_id', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Brother',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.UserProfile')),
                ('brotherhood', models.FloatField(default=0)),
                ('philanthropy', models.FloatField(default=0)),
                ('professional', models.FloatField(default=0)),
                ('gms', models.PositiveIntegerField(default=0)),
                ('attendance_pass', models.CharField(max_length=50)),
                ('excuse', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Pledge',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.UserProfile')),
                ('professional', models.PositiveIntegerField(default=0)),
                ('philanthropy', models.PositiveIntegerField(default=0)),
                ('social', models.PositiveIntegerField(default=0)),
                ('family', models.PositiveIntegerField(default=0)),
                ('brother', models.PositiveIntegerField(default=0)),
                ('pledge', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='chapter_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Chapter'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='events',
            field=models.ManyToManyField(to='app.Event'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='meetings',
            field=models.ManyToManyField(to='app.Meeting'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]