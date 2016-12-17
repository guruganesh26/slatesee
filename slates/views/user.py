from slates.models import User, School
from django.http import Http404

from slates.serializer import UserSerializer
from slates.service import uploadfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UserList(APIView):
    """
    List all users, or create a new user.
    """
    
    def get(self, request, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user_type = request.query_params.get('user_type', None)
        users = User.objects.filter(user_type=user_type, teacher_id=request.user.id)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def is_space_available(self, upload_size):
        school = self.school
        remaining_space = school.disk_space - school.disk_space_used
        print upload_size, remaining_space
        if upload_size < remaining_space:
            return True
        else:
            return False

    def update_used_space(self, file_size):
        school = self.school
        school.disk_space_used += file_size
        school.save()        

    def post(self, request, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if 'created_by' not in request.data:
            request.data['created_by'] = request.user.id
        if request.data['profile_image']:
            if request.user.user_type == 'teacher':
                self.school= School.objects.get(principal=request.user.teacher_id)
            elif request.user.user_type == 'principal':
                self.school = School.objects.get(principal=request.user.id)
            school_id=1
            if self.school:
                school_id =self.school.id
            urls = uploadfile.upload_files(request.data['profile_image'], school_id, self.is_space_available, 
            self.update_used_space, True)
            print urls
            if urls:
                request.data['profile_image'] = urls[0]
        request.data["teacher_id"] = request.user.id
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = self.get_object(pk)
        user = UserSerializer(user)
        return Response(user.data)

    def put(self, request, pk, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            if request.data['password']:
                user.set_password(user.password)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)