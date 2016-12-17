from slates.models import Events, School, User
from django.http import Http404
from slates.service import uploadfile

from slates.serializer import EventSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



class  EventUpload(APIView):

    def get_school(self, teacher_id):
        principal_id = User.objects.get(pk=teacher_id).teacher_id
        self.school = School.objects.get(principal=principal_id)

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
        files = request.data['file_list']
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if request.user.user_type not in ["teacher", "principal"]:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.get_school(request.user.id)
        if 'created_by' not in request.data:
            request.data['created_by'] = request.user.id
        if not request.data['organizer']:
            request.data['organizer'] = request.user.id
        if files:
            urls = uploadfile.upload_files(files, self.school.id, self.is_space_available, 
            self.update_used_space)
            if urls == "NOT_ENOUGH_SPACE":
                Response(serializer.errors, status="Not enough disk space")
            imgs = urls[0].split(',')
            rdata = []

            for i in imgs:
                d = {k:v for k,v in request.data.items()}
                del d["file_list"]
                d['image_url'] = i
                rdata.append(d)
            sout = []
            for r in rdata:
                serializer = EventSerializer(data=r)
                if serializer.is_valid():
                    serializer.save()
                    sout.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(sout, status=status.HTTP_201_CREATED)
        else:
            serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class EventsList(APIView):
    """
    List all Events, or create a new Events.
    """
    def get(self, request, format=None):
        events = Events.objects.filter(organizer=request.user.teacher_id)
        serializer = EventSerializer(events, many=True)
        result = []
        for e in serializer.data:
            orgr = User.objects.get(pk=e["organizer"])
            e["organizer"] = orgr.get_full_name()
            result.append(e)
        return Response(result)

    def post(self, request, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if request.user.user_type not in ["teacher", "principal"]:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        school_id = 1
        school = School.objects.get(principal=request.user.teacher_id)
        if school:
            school_id = school.id
        files = request.data['file_list']
        if 'created_by' not in request.data:
            request.data['created_by'] = request.user.id
        if 'organizer' not in request.data:
            request.data['organizer'] = request.user.id
        if files:
            urls = uploadfile.upload_files(files, school_id, self.is_space_available, 
            self.update_used_space)
            if urls == "NOT_ENOUGH_SPACE":
                Response(serializer.errors, status="Not enough disk space")
            imgs = values[0].split(',')
            rdata = []
            d = {k:v for k,v in request.data[0]}
            for i in imgs:
                d['image_url'] = i
                rdata.append(d)
            serializer = EventSerializer(data=rdata)
        else:
            serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        events = self.get_object(pk)
        events.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EventsDetail(APIView):
    """
    Retrieve, update or delete a Events instance.
    """
    def get_object(self, pk):
        try:
            return Events.objects.get(pk=pk)
        except Events.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        events = self.get_object(pk)
        events = EventSerializer(events)
        return Response(events.data)

    def put(self, request, pk, format=None):
        events = self.get_object(pk)
        serializer = EventSerializer(events, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        events = self.get_object(pk)
        events.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)