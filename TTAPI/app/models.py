from __future__ import unicode_literals

from django.db import models

#to extend the user class of rest_auth app
from django.contrib.auth.models import User

#chapter class
class Chapter(models.Model):
    chapter_id = models.AutoField(primary_key=True)
    #TODO add more chapters if they want to use the API
    CHAPTER_CHOICES = [
            ('K', 'Kappa')
    ]
    chapter_name = models.CharField(max_length=2, choices = CHAPTER_CHOICES, default='K')
    university = models.CharField(max_length = 100)


#user class
class UserProfile(models.Model):
    #predefined user model
    user = models.OneToOneField(User)

    #custom fields for user
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 50)

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

    officer = models.BooleanField(default=False)

    create_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['chapter', 'name']


#Pledge class
class Pledge(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    #for signatures
    professional = models.PositiveIntegerField(default=0)
    philanthropy = models.PositiveIntegerField(default=0)
    social = models.PositiveIntegerField(default=0)
    family = models.PositiveIntegerField(default=0)
    brother = models.PositiveIntegerField(default=0)
    pledge = models.PositiveIntegerField(default=0)

#Brother class
class Brother(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    #event attendance
    brotherhood = models.PositiveIntegerField(default=0)
    philanthropy = models.PositiveIntegerField(default=0)
    professional = models.PositiveIntegerField(default=0)

    #gm stuff
    gms = models.PositiveIntegerField(default=0)



