from slates.models import MCQ, McqSets

from rest_framework import serializers

class MCQSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCQ
        fields = ('id', 'set_id', 'question', 'option1', 'option2', 'option3', 'option4',
        	'answer', 'correct_text', 'wrong_text')

class MCQSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = McqSets
        fields = ('id', 'set_name', 'is_approved', 'created_by', 'updated_by')