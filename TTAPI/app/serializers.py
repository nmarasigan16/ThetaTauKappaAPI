from rest_framework import serializers
from app.models import Chapter, Event, Meeting, Pledge, Brother, Demographics, Hours
from app.models import UserProfile as User

#for rest_auth user
from rest_auth.serializers import UserDetailsSerializer

#TODO make create methods for user that automatically spawns a demographics object, and make a
#create method for demographics that automatically creates either a pledge or brother object


class ChapterSerializer(serializers.ModelSerializer):
    members = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='userprofile-detail')
    class Meta:
        model = Chapter
        fields = ('chapter_id', 'chapter_name', 'university', 'members')

class DemographicsSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    events = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    meetings = serializers.SlugRelatedField(many=True, read_only=True,  slug_field='date')
    class Meta:
        model = Demographics
        fields = ('user', 'name', 'email',  'major', 'status', 'city', 'events', 'meetings')


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
    class Meta:
        model = Hours
        fields = ('user', 'brotherhood', 'professional', 'philanthropy')

class UserSerializer(UserDetailsSerializer):

    id = serializers.IntegerField(read_only=True)
    chapter_id = serializers.PrimaryKeyRelatedField(read_only=True)
    create_date = serializers.DateTimeField(read_only=True)
    demographics = DemographicsSerializer()
    hours = HourSerializer(read_only=True)
    pledge = PledgeSerializer(read_only=True)
    brother = BrotherSerializer(read_only=True)

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('id', 'chapter_id', 'create_date', 'demographics', 'hours', 'brother', 'pledge')

    #TODO make create method to spawn demographics and hours instances
    def create(self, validated_data):
        d_data = validated_data.pop('demographics')
        #create user here
        user = User.objects.create(**validated_data)
        Demographics.objects.create(user=user, **d_data)
        Hours.objects.create(user=user)
        if d_data['status'] == 'P':
            Pledge.objects.create(user=user)
        elif d_data['status'] == 'B':
            Brother.objecfts.create(user=user)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userprofile', {})
        id = profile_data.get('id')
        chapter_id = profile_data.get('chapter_id')
        create_date = profile_data.get('create_date')

        instance = super(UserSerializer, self).update(instance, validated_data)

        #get and update user profile
        profile = instance.userprofile
        if profile_data and id and chapter_id:
            profile.id = id
            profile.chapter_id = chapter_id
            profile.create_date = create_date
        return instance


