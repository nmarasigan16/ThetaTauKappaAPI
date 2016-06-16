from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail

from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from django.core import serializers
from django.http import Http404
from TTAPI import email_info

#auth stuff
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from app.serializers import (
        UserSerializer, ChapterSerializer, DemographicsSerializer,
        EventSerializer, MeetingSerializer, PledgeSerializer,
        BrotherSerializer, UserDetailsSerializer, EventDetailsSerializer,
        AttendanceSerializer, InterviewSerializer, EmailSerializer
        )
from app.models import Chapter, Event, Meeting, Pledge, Brother, Demographics, Attendance, Interview
from app.models import UserProfile as User

#for permissions
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User as auth_user
from django.contrib.contenttypes.models import ContentType
from app.permissions import IsOfficer, ReadOnly, IsPledge

#external files
import officer_functions, all_functions


permission = Permission.objects.get(codename='officer')
group, created = Group.objects.get_or_create(name='officers')
if created:
    group.permissions.add(permission)

"""
A List of Functions that are included

-Finished Functions(need more extensive testing):
    -Viewset for users to lookup other brothers(in their chapter)
    -Viewset for events for users to lookup events(in their chapter)
    -A test for if a user has a chapter
    -A function to change the chapter of the user
    -Add an event
    -Input a password or excuse for attendance
    -Pledge initiation
    -Delete user
    -Modify user officer status
    -Take attendance for a gm
    -send emails to all users

-TODO Functions
    -Allow interviews to be processed
    -allow excuses to be processed
    -edit user profile

"""

##################################################################################################

"""
Viewsets for authenticated users.  Displays all of the relevent details of an event
for users to look at
"""
#Viewset for finding other brothers
class UserDetailList(generics.ListAPIView):
    permission_classes = (ReadOnly,)
    serializer_class = UserDetailsSerializer
    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(chapter = user.profile.chapter)

class UserDetail(APIView):
    permission_classes = (ReadOnly,)
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserDetailsSerializer(user)
        return Response(serializer.data)

#viewset for events
class EventDetailList(generics.ListAPIView):
    permission_classes = (ReadOnly,)
    serializer_class = EventDetailsSerializer
    def get_queryset(self):
        user = self.request.user
        return Event.objects.filter(chapter = user.profile.chapter)

class EventDetail(APIView):
    permission_classes = (ReadOnly,)
    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = EventDetailsSerializer(event)
        return Response(serializer.data)

#viewset for
class InterviewDetailList(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsPledge)
    serializer_class = InterviewSerializer
    def get_queryset(self):
        pledge = self.request.user.profile.pledge
        return Interview.objects.filter(pledge=pledge)

##########################################################################################################
"""
TODO: rewrite register serializer so that way we can register without needing this
This function is for when we want to add a user to a chapter.  This ideally should happen right after the first
login by checking if the user has a chapter
@param:
    a request
@return:
    a json message that gives the chapter status of the user
"""
@api_view(['GET'])
def has_chapter(request):
    permission_classes = (IsAuthenticated,)
    try:
        chapterless = not (request.user.profile.chapter != None)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response({'has_chapter': '%r' % (False if chapterless else True)}, status=status.HTTP_200_OK)

"""
Function to change the chapter of the current user
@param:
    primary key of a chapter object to assign user to
@return:
    response indicating if successful
"""
@api_view(['PUT'])
def change_chapter(request, pk):
    permission_classes = (IsAuthenticated,)
    try:
        profile = request.user.profile
        chapter = Chapter.objects.get(pk=pk)
    except Chapter.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        profile.chapter = chapter
        profile.save()
        chapter.save()
        return Response(create_msg_dict('User %s added to Chapter %s' % (profile.demographics.name, chapter.chapter_name)), status = status.HTTP_200_OK)

############################################################################################################
"""
All Accessible Functions: By brothers and exec
- Add an event/in turn add hours
- Input an attendence password
- Check hours
- add pledge family event (pledges only)
- add signatures (pledges only)
"""

"""
Used by a user to get the requirements that they have fulfilled
@return:
    a dictionary with the appropriate requirements as keys and the amount they've fulfilled as values
"""
@api_view(['GET'])
def check_reqs(request):
    permission_classes = (IsAuthenticated,)
    try:
        user = request.user.profile
    except user.profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        reqs = all_functions.format_reqs(user)
        return Response(reqs, status=status.HTTP_200_OK)
"""
Adds an event to the users events that they've attended and updates their hours
@return:
    message indicating status of the add
"""
@api_view(['GET'])
def add_event(request, pke, hours):
    permission_classes = (IsAuthenticated,)
    try:
        user = request.user.profile
        event = Event.objects.get(pk = pke)
    except user.profile.DoesNotExist or Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        outcome = all_functions.adder(user, event, hours)
        return Response(create_msg_dict(create_msg_dict("Event %s added for user %s" % (event.name, user.email))), status=status.HTTP_200_OK)

"""
Allows pledges to edit and look at the interviews that they have input
@param:
    pk of interview that they want to look at or edit
@return:
    updated interview or interview that has the pk
"""
#TODO make this a RetrieveUpdateAPIView
@api_view(['GET', 'PUT'])
def edit_interview(request, pk):
    permission_classes = (IsPledge, IsOwner,)
    def get_object(self, pk):
        try:
            return Interview.objects.get(pk=pk)
        except Interview.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        interview = get_object(pk)
        serializer = InterviewSerializer(interview)
        return Response(serializer.data)

    def put(self, request, pk, format = None):
        interview = get_object(pk)
        serializer = InterviewSerializer(interview, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
Allows pledges to log their interviews
@return:
    Success or errors generated by the serializer
"""
class LogInterview(generics.CreateAPIView):
    permission_classes = (IsPledge,)
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        interview = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(create_msg_dict("Interview logged"), status=status.HTTP_201_CREATED, headers=headers)
    def perform_create(self, serializer):
        interview = serializer.save(self.request)
        return interview
"""
Allows brothers to input the gm password
@return:
    Success or errors in the update
"""
class AttendanceDetail(APIView):
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
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        meeting = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(create_msg_dict("meeting created"), status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        meeting = serializer.save(self.request)
        return meeting

"""
'Initiates' pledges.
Actually deletes their pledge instance with their pledge requirements
and replaces it with a new brother instance
@param:
    chapter of the chapter whose pledges we want to initiate
@return:
    response indicating status
"""
@api_view(['GET'])
def initiate_pledges(request):
    permission_classes=(IsOfficer,)
    try:
        chapter = request.user.profile.chapter
    except Chapter.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        demographics_list = Demographics.objects.filter(status='P')
        members = User.objects.filter(chapter=chapter, demographics__in=demographics_list)
        officer_functions.initiate(members)
        return Response(create_msg_dict("Pledges for " + chapter.chapter_name + " intiated"), status=status.HTTP_200_OK)

"""
Checks users password against the password in their attendance object if they are a brother
@param:
    pk of the meeting to take attendance for
@return:
    a list of excuses to process
"""
class TakeAttendance(APIView):
    permission_classes=(IsOfficer,)
    def get_object(self, pk):
        try:
            return Meeting.objects.get(pk=pk)
        except Meeting.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        meeting = self.get_object(pk)
        chapter = request.user.profile.chapter
        demographics_list = Demographics.objects.filter(status='B')
        members = User.objects.filter(chapter=chapter, demographics__in=demographics_list)
        excuses = officer_functions.attendance(members, meeting)
        return Response(excuses, status=status.HTTP_200_OK)

@api_view(['POST'])
def email(request, who):
    permission_classes=(IsOfficer,)
    try:
        chapter = request.user.profile.chapter
        d_list = Demographics.objects.filter(status=who)
        members = User.objects.filter(chapter=chapter, demographics__in=d_list)
    except User.DoesNotExist or Demographics.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        serializer = EmailSerializer(data=request.data)
        recipients = list(set(user.user.email for user in members))
        if serializer.is_valid():
            send_mail(serializer.validated_data['subject'], serializer.validated_data['message'], email_info._user, recipients)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        user.delete()
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
