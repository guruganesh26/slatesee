from slates.models import Messages, User
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from slates.serializer import MessageSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class MessageList(APIView):
    """
    List all messages, or create a new message.
    """
    def get(self, request, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        page = int(request.query_params.get('page', 1))
        page_size = 6
        if request.user.user_type=='student':
            message_type = request.query_params.get('message_type', None)
            message_list = Messages.objects.filter(message_type=message_type, 
            is_approved=1, created_by=request.user.teacher_id)
        elif (request.user.user_type=='teacher' or request.user.user_type=='principal'):
            appr = request.query_params.get('is_approved', 0)
            if request.user.user_type=='teacher':
                creators = [request.user.id]
            if request.user.user_type=='principal':
                creators = [u.id for u in User.objects.filter(teacher_id=request.user.id)]
                creators.append(request.user.id)
            print creators 
            message_list = Messages.objects.filter(is_approved=appr, created_by__in=creators)
        paginator = Paginator(message_list, page_size)
        try:
            messages = paginator.page(page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            messages = paginator.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            messages = paginator.page(paginator.num_pages)
        serializer = MessageSerializer(messages, many=True)
        response_data = serializer.data
        if messages:
            response_data = serializer.data+[{"user_type":request.user.user_type}]
        return Response(response_data)

    def post(self, request, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if request.user.user_type not in ["teacher", "principal"]:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if 'created_by' not in request.data:
            request.data['created_by'] = request.user.id
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        message = self.get_object(pk)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MessageDetail(APIView):
    """
    Retrieve, update or delete a message instance.
    """
    def get_object(self, pk):
        try:
            return Messages.objects.get(pk=pk)
        except Messages.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        message = self.get_object(pk)
        message = MessageSerializer(message)
        return Response(message.data)

    def get_all_data(self, rdata, message):
        data = {k:v for k, v in rdata.items()}
        if not rdata.get('message'):
            data['message'] = message.message
        if not data.get('message_type'):
            data['message_type'] = message.message_type
        return data

    def put(self, request, pk, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        message = self.get_object(pk)
        data = self.get_all_data(request.data, message)
        serializer = MessageSerializer(message, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        message = self.get_object(pk)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)