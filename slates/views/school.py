from slates.models import School, User

from slates.serializer import SchoolSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SchoolList(APIView):
    """
    List all users, or create a new user.
    """
    def get(self, request, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        school = School.objects.all()
        serializer = SchoolSerializer(school, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        principal = request.data['emailid']
        if not principal:
            return Response({"principal":"This field required"}, status=status.HTTP_400_BAD_REQUEST)
        name = request.data['principal']
        user = User.objects.create(user_name=principal, password='abc', first_name=name,
         user_type='principal')
        user.save()
        rdata = {k:v for k,v in request.data.items()}
        rdata['principal'] = user.id
        rdata['disk_space'] = 1000000000
        serializer = SchoolSerializer(data=rdata)
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

class SchoolDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    def get_object(self, pk):
        try:
            return School.objects.get(pk=pk)
        except School.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        school = self.get_object(pk)
        school = SchoolSerializer(school)
        return Response(school.data)

    def put(self, request, pk, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = self.get_object(pk)
        serializer = SchoolSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        school = self.get_object(pk)
        school.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)