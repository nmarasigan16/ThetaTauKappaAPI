from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import Group, Permission
from django.core.validators import RegexValidator

#to extend the base user model
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType


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
        ordering = ['chapter_id']

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
    password = models.CharField(max_length=50, blank=True, null=True)
    MEETING_TYPES = [
            ('PM', 'Pledge Meeting'),
            ('GM', 'General Meeting'),
            ('VO', 'Voting'),
            ('IN', 'Initiation'),
    ]
    mtype = models.CharField(max_length=2, choices=MEETING_TYPES, default='GM')
    date = models.DateField()
    attendance_taken = models.BooleanField(default=False)
    chapter =  models.ForeignKey(Chapter, default=0, on_delete=models.CASCADE)


"""
Class for a user

Has attributes:
    -user (to extend the rest_auth user)
    -id (to identify user)
    -chapter (foreign key)
    -create_date (for analytics)
"""
class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, related_name='profile')

    #custom fields for user
    id = models.AutoField(primary_key=True)

    #for which chapter user belongs to
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='members', null=True)

    create_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['chapter_id']
        permissions =(
                ('officer', 'Is an officer'),
            )

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
    name = models.CharField(max_length=30, default="Happy Hour")
    creator = models.ForeignKey(UserProfile, default=0, on_delete=models.SET_DEFAULT, related_name='events')
    date = models.DateField()
    time = models.TimeField()
    duration = models.FloatField(default=0)
    location = models.TextField()
    about = models.TextField()
    EVENT_TYPES = [
            ('PR', 'Professional'),
            ('BR', 'Brotherhood'),
            ('PH', 'Philanthropy'),
    ]

    etype = models.CharField(max_length=2, choices=EVENT_TYPES, default='BR')

    chapter =  models.ForeignKey(Chapter, default=0, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']

"""
Class for demographics.  Holds contact info
Made partially out of laziness, and also partially to abstract passwords and ids from users
Has attributes:
    -name
    -phone number
    -year in school
    -major
    -current status
"""
class Demographics(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True, related_name='demographics')

    name = models.CharField(max_length = 50)

    phone_validator = RegexValidator(regex=r'^[0-9]{9,15}$', message="Phone number needs to be in format 123456789, up to 15 characters accepted")
    phone_number = models.CharField(validators=[phone_validator], max_length=15, blank=True)

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
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True, related_name='pledge')

    #for signatures
    family = models.PositiveIntegerField(default=0)
    brother = models.PositiveIntegerField(default=0)
    pledge = models.PositiveIntegerField(default=0)


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
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True, related_name='brother')


    #gm stuff
    gms = models.PositiveIntegerField(default=0)
    attendance_pass = models.CharField(max_length = 50, blank=True)
    excuse = models.TextField(blank=True)

class Hours(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True, related_name='hours')

    #event attendance
    brotherhood = models.FloatField(default=0)
    philanthropy = models.FloatField(default=0)
    professional = models.FloatField(default=0)
    events = models.ManyToManyField(Event, blank = True, related_name='attendees')
    meetings = models.ManyToManyField(Meeting, blank = True, related_name='attendees')
