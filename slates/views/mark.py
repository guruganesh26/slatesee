from slates.models import Marks
from django.http import Http404

from slates.serializer import MarkSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class MarkList(APIView):
    """
    List all marks, or create a new mark.
    """
    def get(self, request, format=None):
        marks = Marks.objects.all()
        serializer = MarkSerializer(marks, many=True)
        return Response(serializer.data)

    def check_mark_exist(self, request):
        exam_name = request.data.get('exam_name')
        user_id = request.data.get('user_id')
        try:
            mark = Marks.objects.get(pk=user_id, exam_name=exam_name)
        except Marks.DoesNotExist:
            mark = []
        return mark

    def post(self, request, format=None):
        mark = self.check_mark_exist(request)
        if mark:
            serializer = MarkSerializer(mark, data=request.data)
        else:
            serializer = MarkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        mark = self.get_object(pk)
        mark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MarkDetail(APIView):
    """
    Retrieve, update or delete a mark instance.
    """
    def get_object(self, user_id, exam_name):
        try:
            return Marks.objects.get(user_id=user_id, exam_name=exam_name)
        except Marks.DoesNotExist:
            raise Http404

    def get(self, request, user_id, format=None):
        exam_name = request.query_params.get('exam_name', None)
        mark = self.get_object(user_id, exam_name)
        mark = MarkSerializer(mark)
        return Response(mark.data)

    def put(self, request, pk, format=None):
        mark = self.get_object(pk)
        serializer = MarkSerializer(mark, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        mark = self.get_object(pk)
        mark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)