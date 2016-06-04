from rest_framework import serializers
from app.models import Chapter, Event, Meeting, Pledge, Brother, Demographics, Hours, Attendance
from app.models import UserProfile as User
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

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ('password', 'excuse')

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


class EventSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True, default = None)
    chapter = serializers.SlugRelatedField(read_only=True, slug_field='chapter_name', default=None)
    class Meta:
        model = Event
        fields = ('event_id', 'name', 'creator', 'date', 'time', 'duration', 'location', 'about', 'etype', 'chapter')

    def save(self, request):
        creator = request.user.profile
        chapter = request.user.profile.chapter
        validated_data = self.validated_data
        validated_data['creator'] = creator
        validated_data['chapter'] = chapter
        event = Event.objects.create(**validated_data)
        return event

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ('meeting_id', 'password', 'mtype', 'date', 'chapter')

class PledgeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Pledge
        fields = ('user', 'family', 'brother', 'pledge')

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

    class Meta:
        model=User
        fields = ('user', 'id', 'chapter', 'demographics', 'brother', 'pledge', 'attendance')

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
        profile = User.objects.create(user=user)
        data = self.validated_data
        d_data = data['demographics']
        d_data['user']=profile
        Demographics.objects.create(**d_data)
        Hours.objects.create(user=profile)
        Attendance.objects.create(user=profile)
        if d_data['status'] == 'P':
            Pledge.objects.create(user=profile)
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
class UserDetailsSerializer(serializers.Serializer):

    name = serializers.SlugRelatedField(read_only=True, slug_field='name', source='user.profile.demographics')
    email = serializers.SlugRelatedField(read_only=True, slug_field='email', source='user')
    phone_number = serializers.SlugRelatedField(read_only=True, slug_field='phone_number', source='demographics')
    chapter = serializers.SlugRelatedField(read_only=True, slug_field='chapter_name')

    class Meta:
        fields = ('name', 'email', 'phone_number', 'chapter')

class EventDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('name', 'date', 'time', 'location', 'about', 'etype')
