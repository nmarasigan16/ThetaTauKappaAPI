from rest_framework import serializers
from datetime import datetime
from rest_auth.serializers import UserDetailsSerializer
from app.models import Chapter, Event, Meeting, Pledge, Brother, Demographics, Hours, Attendance, Interview, Excuse
from app.models import UserProfile as UserProfile
from django.http import HttpRequest
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

try:
    from allauth.account import app_settings as allauth_settings
    from allauth.utils import (email_address_exists,
                               get_username_max_length)
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
except ImportError:
    raise ImportError('allauth needs to be added to INSTALLED_APPS.')

class EmailSerializer(serializers.Serializer):
    subject=serializers.CharField(style={'base_template': 'textarea.html'})
    message=serializers.CharField(style={'base_template': 'textarea.html'})
    class Meta:
        fields = ('subject', 'message')


class InterviewSerializer(serializers.ModelSerializer):
    pledge = serializers.StringRelatedField(read_only=True, default = None)
    class Meta:
        model = Interview
        fields = ('interview_id', 'pledge', 'brother', 'description')

    def save(self, request):
        pledge = request.user.profile.pledge
        validated_data = self.validated_data
        validated_data['pledge'] = pledge
        interview = Interview.objects.create(**validated_data)
        return interview

class AttendanceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    class Meta:
        model = Attendance
        fields = ('user', 'password', 'excuse')

class ChapterSerializer(serializers.ModelSerializer):
    members = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='userprofile-detail')
    class Meta:
        model = Chapter
        fields = ('chapter_id', 'chapter_name', 'university', 'members')

class DemographicsSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=None, required=False)
    class Meta:
        model = Demographics
        fields = ('user', 'name',  'phone_number', 'major', 'status', 'city')

class ExcuseSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    meeting = serializers.SlugRelatedField(read_only=True, slug_field = 'date')
    class Meta:
        model = Excuse
        fields = ('excuse_id', 'user', 'meeting', 'excuse')

class ExcuseSkeletonSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(source='user')
    class Meta:
        model = Excuse
        fields = ('excuse_id', 'excuse', 'name')

class MeetingSerializer(serializers.ModelSerializer):
    chapter = serializers.SlugRelatedField(read_only=True, required=False, slug_field = 'chapter_name')
    attendees = serializers.StringRelatedField(many=True)
    excuses = ExcuseSkeletonSerializer(many=True)
    class Meta:
        model = Meeting
        fields = ('meeting_id', 'password', 'mtype', 'date', 'chapter', 'attendees', 'excuses')
    def save(self, request):
        chapter = request.user.profile.chapter
        validated_data = self.validated_data
        validated_data['chapter'] = chapter
        meeting = Meeting.objects.create(**validated_data)
        return meeting

class PledgeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    interviews = InterviewSerializer(many=True)
    class Meta:
        model = Pledge
        fields = ('user', 'family', 'brother', 'pledge', 'interviews')

class BrotherSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Brother
        fields = ('user', 'gms')

class HourSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    events = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name', default=[])
    meetings = serializers.SlugRelatedField(many=True, read_only=True,  slug_field='date', default=[])
    class Meta:
        model = Hours
        fields = ('user', 'brotherhood', 'professional', 'philanthropy', 'events', 'meetings')



class UserSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='email', default=None)
    chapter = serializers.SlugRelatedField(read_only=True, slug_field='chapter_name', default=None)
    demographics = DemographicsSerializer()
    brother = BrotherSerializer()
    pledge = PledgeSerializer()
    attendance = AttendanceSerializer()
    hours = HourSerializer()

    class Meta:
        model=UserProfile
        fields = ('user', 'id', 'chapter', 'demographics', 'brother', 'pledge', 'attendance', 'hours')

#overwrites register serializer so that way it spins off a user instance with all the proper things

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=allauth_settings.USERNAME_REQUIRED)
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    demographics = DemographicsSerializer()

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)
    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def custom_signup(self, request, user):
        profile = UserProfile.objects.create(user=user)
        data = self.validated_data
        d_data = data['demographics']
        d_data['user']=profile
        Demographics.objects.create(**d_data)
        Hours.objects.create(user=profile)
        Attendance.objects.create(user=profile)
        if d_data['status'] == 'P':
            pledge = Pledge.objects.create(user=profile)
        elif d_data['status'] == 'B':
            Brother.objects.create(user=profile)

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        setup_user_email(request, user, [])
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        return user


class VerifyEmailSerializer(serializers.Serializer):
    key = serializers.CharField()


"""
All detail serializers.  Useful to view information
"""
class UserDetailsSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(read_only=True, slug_field='name', source='user.profile.demographics')
    email = serializers.SlugRelatedField(slug_field='email', source='user', read_only=True)
    phone_number = serializers.SlugRelatedField(read_only=True, slug_field='phone_number', source='demographics')
    city = serializers.SlugRelatedField(slug_field='city', source='demographics', read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'name', 'email', 'phone_number', 'city')

class EventDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('event_id', 'name', 'date','location', 'about', 'etype')
class EventCreateSerializer(serializers.ModelSerializer):
    creator = UserDetailsSerializer(read_only=True, default = None)
    date = serializers.CharField()
    chapter = serializers.SlugRelatedField(read_only=True, slug_field='chapter_name', default=None)
    class Meta:
        model = Event
        fields = ('event_id', 'name', 'creator', 'date', 'duration', 'location', 'about', 'etype', 'chapter')
    def save(self, request):
        creator = request.user.profile
        chapter = request.user.profile.chapter
        validated_data = self.validated_data
        validated_data['creator'] = creator
        validated_data['chapter'] = chapter

        sdate = validated_data.pop('date')
        year = (int)(sdate[0:4])
        month = (int)(sdate[4:6])
        day = (int)(sdate[6:8])
        hour = (int)(sdate[8:10])
        minute = (int)(sdate[10:12])

        date = datetime(year, month, day, hour, minute)
        validated_data['date'] = date

        event = Event.objects.create(**validated_data)
        return event

class EventSerializer(serializers.ModelSerializer):
    creator = UserDetailsSerializer(read_only=True, default = None)
    chapter = serializers.SlugRelatedField(read_only=True, slug_field='chapter_name', default=None)
    attendees = serializers.StringRelatedField(many=True)
    class Meta:
        model = Event
        fields = ('event_id', 'name', 'creator', 'date', 'duration', 'location', 'about', 'etype', 'chapter', 'attendees')


class ProfileSerializer(UserDetailsSerializer):
    status = serializers.CharField(source='profile.demographics.status')

    class Meta(UserDetailsSerializer.Meta):
        fields = ('status',)
