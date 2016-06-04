from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from django.core import serializers
from django.http import Http404

#auth stuff
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from app.serializers import (
        UserSerializer, ChapterSerializer, DemographicsSerializer,
        EventSerializer, MeetingSerializer, PledgeSerializer,
        BrotherSerializer, UserDetailsSerializer, EventDetailsSerializer,
        AttendanceSerializer
        )
from app.models import Chapter, Event, Meeting, Pledge, Brother, Demographics, Attendance
from app.models import UserProfile as User

#for permissions
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User as auth_user
from django.contrib.contenttypes.models import ContentType
from app.permissions import IsOfficer

#external files
import officer_functions, all_functions


permission = Permission.objects.get(codename='officer')
group, created = Group.objects.get_or_create(name='officers')
if created:
    group.permissions.add(permission)

"""
Viewsets for authenticated users.  Displays all of the relevent details of an event
for users to look at
"""
class UserDetailList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserDetailsSerializer
    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(chapter = user.profile.chapter)
class EventDetailList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventDetailsSerializer
    def get_queryset(self):
        user = self.request.user
        return Event.objects.filter(chapter = user.profile.chapter)


"""
This function is for when we want to add a user to a chapter.  This ideally should happen right after the first
login by checking if the user has a chapter
"""
@api_view(['GET'])
def has_chapter(request):
    permission_classes = (IsAuthenticated,)
    try:
        chapterless = not (request.user.profile.chapter != None)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response({'has_chapter': '%s' % ('False' if chapterless else 'True')}, status=status.HTTP_200_OK)

@api_view(['PUT'])
def change_chapter(request, pk):
    permission_classes = (IsAuthenticated,)
    try:
        profile = request.user.profile
        chapter = Chapter.objects.get(pk=pk)
        profile.chapter = chapter
        profile.save()
        chapter.save()
    except Chapter.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        return Response(create_msg_dict('User %s added to Chapter %s' % (profile.demographics.name, chapter.chapter_name)), status = status.HTTP_200_OK)

"""
All Accessible Functions: By brothers and exec
- Add an event/in turn add hours
- Input an attendence password
- Check hours
- add pledge family event (pledges only)
- add signatures (pledges only)
"""
@api_view(['GET'])
def check_reqs(request):
    permission_classes = (IsAuthenticated,)
    try:
        user = request.user.profile
        reqs = all_functions.format_reqs(user)
    except user.profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request == 'GET':
        return Response(reqs)

@api_view(['PUT'])
def add_event(request, pke, hours):
    permission_classes = (IsAuthenticated,)
    if request.method == 'PUT':
        try:
            user = request.user.profile
            event = Event.objects.get(pk = pke)
            outcome = all_functions.adder(user, event, hours)
        except user.profile.DoesNotExist or Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

#TODO make object permissions for attendance and write attendance view
class AttendanceDetail(APIView):
#TODO make permission class to only allow it to be edited by the owner or officer
    permission_classes = (IsAuthenticated,)
    def get_object(self, user):
        try:
            return Attendance.objects.get(user=user)
        except Attendance.DoesNotExist:
            raise Http404
    def get(self, request, format=None):
        attendance = self.get_object(request.user.profile)
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data)
    def put(self, request, format=None):
        attendance=self.get_object(request.user.profile)
        serializer = AttendanceSerializer(attendance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
Officer only functions:
- Create event
- Take attendance (technically should only happen by scribe, but anyone can do it).
- See event attendance (useful for historian)
- Initiate pledges
"""

class EventViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOfficer,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(create_msg_dict("event created"), status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        event = serializer.save(self.request)
        return event

class MeetingViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOfficer,)
    queryset= Meeting.objects.all()
    serializer_class = MeetingSerializer

"""
'Initiates' pledges.
Actually deletes their pledge instance with their pledge requirements
and replaces it with a new brother instance
@param:
    chapter of the chapter whose pledges we want to initiate
@return:
    response indicating status
"""
@api_view(['PUT'])
def initiate_pledges(request, pk):
    permission_classes=(IsOfficer,)
    if request.method == 'PUT':
        try:
            chapter = Chapter.objects.get(pk=pk)
            members = chapter.members.all()
            officer_functions.initiate(members)
        except Chapter.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(create_msg_dict("Pledges for " + chapter.chapter_name + " intiated"), status=status.HTTP_200_OK)

"""
Admin only functions and viewsets
Only those that have the .is_staff in their
Django user can access these functions
"""

class DemographicsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = Demographics.objects.all()
    serializer_class = DemographicsSerializer


class ChapterViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

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


"""
change user officer status
@param:
    pk of the person to be added to the officers
    status.  1 is to add an officer, 0 indicates to remove an officer, 273 indicates removal of all officers
@return:
    success or failure and the type of operation in a json message
"""
@api_view(['GET'])
def modify_officer_status(request, pk, operation):
    permission_classes=(IsAdminUser,)
    try:
        user=(User.objects.get(pk=pk)).user
        group = Group.objects.get(name='officers')
        if operation == '1':
            group.user_set.add(user)
        elif operation == '0':
            group.user_set.remove(user)
        elif operation == '273':
            group.user_set.clear()
        else:
            return Response(create_msg_dict(
                "Please use a 1 or a 0 to indicate the operation on the user"
                ),
                status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        return Response(create_msg_dict('Officer status for user %s changed' % user.profile.demographics.name),
                status=status.HTTP_200_OK)

def create_msg_dict(msg):
    return {'message':msg}
