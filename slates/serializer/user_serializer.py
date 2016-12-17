from slates.models import User

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'user_name', 'password', 'first_name', 
        	'standard', 'profile_image', 'parent_name', 'mobile_no', 
        	'teacher_id','dob', 'reg_no', 'user_type')