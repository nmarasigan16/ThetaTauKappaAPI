from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from rest_framework import status, generics, permissions
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

#for permissions
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User as auth_user
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.get_for_model(auth_user)
permission = Permission.objects.get_or_create(codename='officer', name='Is an officer', content_type=content_type)
group, created = Group.objects.get_or_create(name='officers')
if created:
    group.permissions.add(permission)

#external files
import officer_functions, all_functions

#TODO import functions from other files

"""
Permissions classes.
Used to determine whether or not someone is an officer before they can access certain functions
"""
class IsOfficer(permissions.BasePermission):
    def has_object_permission(self, request):
        if request.method in permission.SAFE_METHODS:
            return True
        return request.user.has_permissions(app.officer)


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
    permission_classes = (IsAdminUser,)
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
"""

"""
This view is for posting events
"""
class EventDetailCreate(generics.CreateAPIView):
    permission_classes = (IsOfficer,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventDetailDestroy(generics.DestroyAPIView):
    permission_classes = (IsOfficer,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventDetailUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = (IsOfficer,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer
"""
This is for meetings
Same note as events
"""
class MeetingDetailCreate(generics.CreateAPIView):
    permission_classes= (IsOfficer,)
    queryset = Event.objects.all()
    serializer_class = MeetingSerializer

class MeetingDetailUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = (IsOfficer,)
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

class MeetingDetailDestroy(generics.DestroyAPIView):
    permission_classes = (IsOfficer,)
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

"""
'Initiates' pledges.
Actually deletes their pledge instance with their pledge requirements
and replaces it with a new brother instance
@param:
    chapter_id of the chapter whose pledges we want to initiate
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
Admin only functions
Only those that have the .is_staff in their
Django user can access these functions
"""


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
@api_view(['PUT'])
def modify_officer_status(request, pk, operation):
    permission_classes=(IsAdminUser,)
    try:
        user=User.objects.get(pk=pk)
        group = Group.objects.get(name='officers')
        if operation == 1:
            group.user_set.add(user)
        elif operation == 0:
            group.user_set.remove(user)
        elif operation == 273:
            group.user_set.clear()
        else:
            return Response(create_msg_dict(
                "Please use a 1 or a 0 to indicate the operation on the user"
                ),
                status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        return Response(create_msg_dict('Officer status for user %s changed' % user.demographics.name),
                status=status.HTTP_200_OK)

def create_msg_dict(msg):
    return {'message':msg}
