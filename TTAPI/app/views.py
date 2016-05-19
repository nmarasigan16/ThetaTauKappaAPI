from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from django.core import serializers

from app.serializers import UserSerializer, ChapterSerializer
from app.models import Chapter, Event, Meeting, Pledge, Brother
from app.models import UserProfile as User


"""
Temporary functions for testing

These functions are just for testing insertion and deletion from the API
and will be commented out or deleted once testing is complete

"""
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
