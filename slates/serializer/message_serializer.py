from slates.models import Messages

from rest_framework import serializers

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ('id', 'message', 'message_type', 'is_approved', 'created_by', 'updated_by')