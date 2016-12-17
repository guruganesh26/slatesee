from slates.models import School

from rest_framework import serializers

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('school_name', 'principal', 'no_of_students', 'no_of_teachers', 'disk_space')