from __future__ import unicode_literals

from django.db import models

#to extend the user class of rest_auth app
from django.contrib.auth.models import User

"""
Chapter class

Has attributes:
    -chapter_id
    -chapter_name
    -university
"""
class Chapter(models.Model):
    chapter_id = models.AutoField(primary_key=True)
    #TODO add more chapters if they want to use the API
    CHAPTER_CHOICES = [
            ('K', 'Kappa')
    ]
    chapter_name = models.CharField(max_length=2, choices = CHAPTER_CHOICES, default='K')
    university = models.TextField()

"""
Event class

Has attributes:
    -event_id (pk)
    -date
    -type (professional, philanthropy, brotherhood)
    -location
    -about
"""
class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.TextField()
    about = models.TextField()


"""
Meeting class

Has attributes:
    -meeting_id
    -mtype
    -date
"""
class Meeting(models.Model):
    meeting_id = models.AutoField(primary_key=True)
    MEETING_TYPES = [
            ('PM', 'Pledge Meeting'),
            ('GM', 'General Meeting'),
            ('VO', 'Voting'),
            ('IN', 'Initiation'),
    ]
    mtype = models.CharField(max_length=2, choices=MEETING_TYPES, default='GM')
    date = models.DateField()


"""
Class for a user

Has attributes:
    -user (to extend the rest_auth user)
    -id (to identify user)
    -name
    -chapter_id (foreign key)
    -year in school
    -major
    -current status
    -whether or not they are an officer
    -create_date (for analytics)
"""
class UserProfile(models.Model):
    #predefined user model
    user = models.OneToOneField(User)

    #custom fields for user
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 50)

    #for which chapter user belongs to
    chapter_id = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    YEAR_IN_SCHOOL_CHOICES = [
            ('FR', 'Freshman'),
            ('SO', 'Sophomore'),
            ('JR', 'Junior'),
            ('SR', 'Senior'),
            ('AL', 'Alum'),
    ]
    year = models.CharField(max_length=2, choices=YEAR_IN_SCHOOL_CHOICES, default = 'FR')

    MAJOR_CHOICES = [
            ('AE', 'Aerospace Engineering'),
            ('AB', 'Agricultural and Biological Engineering'),
            ('BE', 'Bioengineering'),
            ('CH', 'Chemical Engineering'),
            ('CE', 'Civil Engineering'),
            ('CO', 'Computer Engineering'),
            ('CS', 'Computer Science'),
            ('EE', 'Electrical Engineering'),
            ('GE', 'General Engineering'),
            ('IE', 'Industrial Engineering'),
            ('MA', 'Materials Science and Engineering'),
            ('ME', 'Mechanical Engineering/Engineering Mechanics'),
            ('NE', 'Nuclear, Plasma, and Radiological Engineering'),
            ('UE', 'Undeclared Engineering'),
    ]
    major = models.CharField(max_length=2, choices=MAJOR_CHOICES, default='UE')

    STATUS_CHOICES = [
            ('P', 'Pledge'),
            ('B', 'Brother'),
            ('A', 'Alumni'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='B')

    events = models.ManyToManyField(Event)
    meetings = models.ManyToManyField(Meeting)

    officer = models.BooleanField(default=False)

    create_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['chapter_id', 'name']

"""
Class for pledges
Extends the UserProfile class

Gives additional attributes:
    -professional
    -philanthropy
    -social
    -family
    -brother
    -pledge

Each represents a number of signatures/events
that a pledge needs to attend to become a brother
"""
class Pledge(models.Model):
    #extends user class
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True)

    #for signatures
    professional = models.PositiveIntegerField(default=0)
    philanthropy = models.PositiveIntegerField(default=0)
    social = models.PositiveIntegerField(default=0)
    family = models.PositiveIntegerField(default=0)
    brother = models.PositiveIntegerField(default=0)
    pledge = models.PositiveIntegerField(default=0)

    #make it easy for historian to track all events

"""
Class for brothers
Extends UserProfile class

Gives additional attributes:
    #used to let brothers track hours
    -brotherhood
    -philanthropy
    -professional
    -gms

    #used for gm attendance, wiped out after scribe takes attendance
    -attendance password
    -excuse

"""
class Brother(models.Model):
    #extends user class
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True)

    #event attendance
    brotherhood = models.FloatField(default=0)
    philanthropy = models.FloatField(default=0)
    professional = models.FloatField(default=0)

    #gm stuff
    gms = models.PositiveIntegerField(default=0)
    attendance_pass = models.CharField(max_length = 50)
    excuse = models.TextField()


