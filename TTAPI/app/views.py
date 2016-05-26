from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from django.core import serializers

#auth stuff
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from app.serializers import (
        UserSerializer, ChapterSerializer, DemographicsSerializer,
        EventSerializer, MeetingSerializer, PledgeSerializer,
        BrotherSerializer
        )
from app.models import Chapter, Event, Meeting, Pledge, Brother, Demographics
from app.models import UserProfile as User

#TODO import functions from other files


"""
Temporary functions for testing

These functions are just for testing insertion and deletion from the API
and will be commented out or deleted once testing is complete

EDIT 5/25:
    UserViewSet will allow us to view all brothers and thus will not be removed after testing
    as will Chapter viewset.  It'd probably be a useful feature going forward if this API spreads
    to other chapters

"""
class DemographicsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Demographics.objects.all()
    serializer_class = DemographicsSerializer


class ChapterViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer


"""
All Accessible Functions: By brothers and exec
- Add an event/in turn add hours
- Input an attendence password
- Check hours
- add pledge family event (pledges only)
- add signatures (pledges only)
"""

#TODO implement these functions


"""
Officer only functions:
- Create event
- Take attendance (technically should only happen by scribe, but anyone can do it).
- See event attendance (useful for historian)
- Initiate pledges
- Delete user (in case drops)
"""
@api_view(['GET'])
def check_officer(request, pk):
    permission_classes = (IsAuthenticated,)
    try:
        bro = Brother.get(pk=pk)
        is_officer = bro.officer
    except Brother.DoesNotExist:
        return response(status=status.HTTP_404_NOT_FOUND)
   if request.method == 'GET':
       if is_officer
           return response(status=status.HTTP_200_OK)
       else
           return response(status=status.HTTP_403_FORBIDDEN)

"""
This view is for posting events
NOTE:
    I would like to make this so that only
    officers can post events. At the moment
    any user that is logged in can create events
"""
class EventDetailCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventDetailDestroy(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventDetailUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer
"""
This is for meetings
Same note as events
"""
class MeetingDetailCreate(generics.CreateAPIView):
    permission_classes= (IsAuthenticated,)
    queryset = Event.objects.all()
    serializer_class = MeetingSerializer



#TODO initiate pledges
#can delete with a for loop and .delete, but how to create multiple users?

