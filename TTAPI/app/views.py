from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from rest_framework import status, generics
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
        BrotherSerializer, UserDetailsSerializer
        )
from app.models import Chapter, Event, Meeting, Pledge, Brother, Demographics
from app.models import UserProfile as User

#external files
import officer_functions, all_functions

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
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer

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
@api_view(['GET'])
def check_reqs(request, pk):
    permission_classes = (IsAuthenticated,)
    try:
        user = User.objects.objects.get(pk=pk)
        reqs = all_functions.format_reqs(user)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request == 'GET':
        return Response(reqs)

@api_view(['PUT'])
def add_event(request, pku, pke, hours):
    permission_classes = (IsAuthenticated,)
    if request.method == 'PUT':
        try:
            user = User.objects.get(pk = pku)
            event = Event.objects.get(pk = pke)
            outcome = all_functions.adder(user, event, hours)
        except User.DoesNotExist or Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

"""
Officer only functions:
- Create event
- Take attendance (technically should only happen by scribe, but anyone can do it).
- See event attendance (useful for historian)
- Initiate pledges
- Delete user (in case drops)
"""

"""
Check if user is an officer
@param:
    request type
    id of user to check
@return
    status of request
"""
@api_view(['GET'])
def check_officer(request, pk):
    permission_classes = (IsAuthenticated,)
    try:
        bro = Brother.objects.get(pk=pk)
        is_officer = bro.officer
    except Brother.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        if is_officer:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

"""
This view is for posting events
NOTE:
    I would like to make this so that only
    officers can post events. At the moment
    any user that is logged in can create
    and edit events.  Also see if I can determine owner
"""
class EventDetailCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventDetailDestroy(generics.DestroyAPIView):
    permission_classes = (IsAdminUser,)
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

class MeetingDetailUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

class MeetingDetailDestroy(generics.DestroyAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

"""
Delete user function
@param
    type of request
    id of user to be deleted
@return
    response determining if user was deleted or dne
"""
@api_view(['DELETE'])
def delete_user(request, pk):
    permission_classes=(IsAdminUser,)
    if request.method == 'DELETE':
        try:
            user = User.objects.get(pk=pk)
            user.delete()
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(create_msg_dict("User deleted"), status=status.HTTP_200_OK)

@api_view(['PUT'])
def initiate_pledges(request, pk):
    permission_classes=(IsAdminUser,)
    if request.method == 'PUT':
        try:
            chapter = Chapter.objects.get(pk=pk)
            members = chapter.members.all()
            officer_functions.initiate(members)
        except Chapter.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(create_msg_dict("Pledges for " + chapter.chapter_name + " intiated"), status=status.HTTP_200_OK)


def create_msg_dict(msg):
    return {'message':msg}
