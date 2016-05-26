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
    class Meta:
        ordering = ['chapter_name']

"""
Meeting class

Has attributes:
    -meeting_id
    -password
    -mtype
    -date
"""
class Meeting(models.Model):
    meeting_id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=50, default="passionfruit")
    MEETING_TYPES = [
            ('PM', 'Pledge Meeting'),
            ('GM', 'General Meeting'),
            ('VO', 'Voting'),
            ('IN', 'Initiation'),
    ]
    mtype = models.CharField(max_length=2, choices=MEETING_TYPES, default='GM')
    date = models.DateField()
    attendance_taken = models.BooleanField(default=False)


"""
Class for a user

Has attributes:
    -user (to extend the rest_auth user)
    -id (to identify user)
    -chapter_id (foreign key)
    -create_date (for analytics)
"""
class UserProfile(models.Model):
    #predefined user model
    user = models.OneToOneField(User)

    #custom fields for user
    id = models.AutoField(primary_key=True)

    #for which chapter user belongs to
    chapter_id = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    create_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['chapter_id']

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
    creator = models.ForeignKey(UserProfile, default=0, on_delete=models.SET_DEFAULT)
    date = models.DateField()
    time = models.TimeField()
    location = models.TextField()
    about = models.TextField()


"""
Class for demographics.  Holds contact info
Made partially out of laziness, and also partially to abstract passwords and ids from users
Has attributes:
    -name
    -year in school
    -major
    -current status
"""
class Demographics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length = 50)

    email = models.EmailField(null=True)

    #TODO add phone number regex

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
    city = models.CharField(max_length=30, blank=True)

    events = models.ManyToManyField(Event, blank = True)
    meetings = models.ManyToManyField(Meeting, blank = True)

    class Meta:
        ordering = ['name']


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

    #used for status
    -officer

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
    attendance_pass = models.CharField(max_length = 50, blank=True)
    excuse = models.TextField(blank=True)

    #officer status
    officer = models.BooleanField(default=False)

