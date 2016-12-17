from slates.models import FlashCard

from rest_framework import serializers

class FlashCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashCard
        fields = ('id', 'side_a', 'side_b', 'is_approved', 'created_by', 'updated_by')