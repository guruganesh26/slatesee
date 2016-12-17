from slates.models import Marks

from rest_framework import serializers

class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marks
        fields = ('user_id', 'exam_name', 's1', 's2', 's3','s4','s5', 'updated_by')