from rest_framework import serializers
from app.models import Chapter, Event, Meeting, Pledge, Brother
from app.models import UserProfile as User

#for rest_auth user
from rest_auth.serializers import UserDetailsSerializer

class UserSerializer(UserDetailsSerializer):

    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = UserDetailsSerializer.Meta.fields + (
                'id', 'name', 'chapter_id', 'year', 'major',
                'status', 'events', 'meetings', 'create_date')
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userprofile', {})
        id = profile_data.get('id')
        name = profile_data.get('name')
        chapter_id = profile_data.get('chapter_id')
        year = profile_data.get('year')
        major = profile_data.get('major')
        status = profile_data.get('status')
        events = profile_data.get('events')
        meetings = profile_data.get('meetings')

        instance = super(UserSerializer, self).update(instance, validated_data)

        #get and update user profile
        profile = instance.userprofile
        if profile_data and id and name and chapter_id and year and major and status and events and meetings:
            profile.id = id
            profile.name = name
            profile.chapter_id = chapter_id
            profile.year = year
            profile.major = major
            profile.status = status
            profile.events = events
            profile.meetings = meetings
        return instance
