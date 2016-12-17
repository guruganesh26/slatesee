from slates.models import MCQ, User, McqSets
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from slates.serializer import MCQSerializer, MCQSetSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class MCQList(APIView):
    """
    List all mcqs, or create a new mcq.
    """
    def get(self, request, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        page = int(request.query_params.get('page', 1))
        set_id = int(request.query_params.get('set_id', 1))
        page_size = 6
        if request.user.user_type=='student':
            mcq_list = MCQ.objects.filter(set_id=set_id)
        elif (request.user.user_type=='teacher' or request.user.user_type=='principal'):
            #appr = request.query_params.get('is_approved', 0)
            mcq_list = MCQ.objects.filter(set_id=set_id)
        paginator = Paginator(mcq_list, page_size)
        try:
            mcqs = paginator.page(page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            mcqs = paginator.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            mcqs = paginator.page(paginator.num_pages)
        serializer = MCQSerializer(mcqs, many=True)
        response_data = serializer.data
        if mcqs:
            response_data = serializer.data+[{"user_type":request.user.user_type}]
        return Response(response_data)

    def post(self, request, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if request.user.user_type not in ["teacher", "principal"]:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if 'set_id' not in request.data:
            if 'set_name' in request.data:
                mcq_set = McqSets.objects.create(set_name=request.data['set_name'], is_approved=0, 
                    created_by=request.user, updated_by=request.user)
                mcq_set.save()
                request.data['set_id'] = mcq_set.id
            else:
                return Response({"set_name":"This field is required"}, 
                    status=status.HTTP_400_BAD_REQUEST)
        serializer = MCQSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        mcq = self.get_object(pk)
        mcq.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MCQDetail(APIView):
    """
    Retrieve, update or delete a mcq instance.
    """
    def get_object(self, pk):
        try:
            return MCQ.objects.get(pk=pk)
        except MCQ.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        mcq = self.get_object(pk)
        mcq = MCQSerializer(mcq)
        return Response(mcq.data)

    def put(self, request, pk, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        mcq = self.get_object(pk)
        serializer = MCQSerializer(mcq, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        mcq = self.get_object(pk)
        mcq.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MCQSetList(APIView):
    """
    List all mcqs, or create a new mcq.
    """
    def get(self, request, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        page = int(request.query_params.get('page', 1))
        page_size = 6
        if request.user.user_type=='student':
            mcq_list = McqSets.objects.filter( is_approved=1, 
                created_by=request.user.teacher_id)
        elif (request.user.user_type=='teacher' or request.user.user_type=='principal'):
            appr = request.query_params.get('is_approved', 0)
            if request.user.user_type=='teacher':
                creators = [request.user.id]
            if request.user.user_type=='principal':
                creators = [u.id for u in User.objects.filter(teacher_id=request.user.id)]
                creators.append(request.user.id)
            if request.query_params.get('all', None):
                mcq_list = McqSets.objects.all()
            else:
                mcq_list = McqSets.objects.filter(is_approved=appr, created_by__in=creators)
        print request.data
        if not request.query_params.get('all', None):
            print "inside all"
            paginator = Paginator(mcq_list, page_size)
            try:
                mcqs = paginator.page(page)
            except PageNotAnInteger:
            # If page is not an integer, deliver first page.
                mcqs = paginator.page(1)
            except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
                mcqs = paginator.page(paginator.num_pages)
        else:
            mcqs = mcq_list
        print mcqs
        serializer = MCQSetSerializer(mcqs, many=True)
        response_data = serializer.data
        if mcqs:
            response_data = serializer.data+[{"user_type":request.user.user_type}]
        return Response(response_data)