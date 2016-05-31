from rest_framework import serializers
from app.models import Chapter, Event, Meeting, Pledge, Brother, Demographics, Hours
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


#for rest_auth user

#TODO make create methods for user that automatically spawns a demographics object, and make a
#create method for demographics that automatically creates either a pledge or brother object


class ChapterSerializer(serializers.ModelSerializer):
    members = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='userprofile-detail')
    class Meta:
        model = Chapter
        fields = ('chapter_id', 'chapter_name', 'university', 'members')

class DemographicsSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=None, required=False)
    class Meta:
        model = Demographics
        fields = ('user', 'name', 'email',  'major', 'status', 'city')


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('event_id', 'name', 'creator', 'date', 'time', 'duration', 'location', 'about', 'etype', 'chapter')

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
        fields = ('user', 'gms', 'attendance_pass', 'excuse', 'officer')

class HourSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    events = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name', default=[])
    meetings = serializers.SlugRelatedField(many=True, read_only=True,  slug_field='date', default=[])
    class Meta:
        model = Hours
        fields = ('user', 'brotherhood', 'professional', 'philanthropy', 'events', 'meetings')

class UserSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username', default=None)
    chapter_id = serializers.SlugRelatedField(read_only=True, slug_field='chapter_name', default=None)
    class Meta:
        model=User
        fields = ('user', 'id', 'chapter_id')

#overwrites register serializer so that way it spins off a user instance with all the proper things

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=allauth_settings.USERNAME_REQUIRED
    )
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    demographics = DemographicsSerializer()


    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

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

    user = serializers.SlugRelatedField(read_only=True, slug_field='username', default=None)
    demographics = DemographicsSerializer(read_only=True, default=None)
    hours = HourSerializer(read_only=True, default=None)
    pledge = PledgeSerializer(read_only=True)
    brother = BrotherSerializer(read_only=True)

    class Meta:
        fields = ('user', 'create_date', 'demographics', 'hours', 'brother', 'pledge')
