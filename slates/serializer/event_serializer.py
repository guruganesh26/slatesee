from slates.models import Events

from rest_framework import serializers

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ('event_detail', 'image_url', 'organizer', 'event_date')