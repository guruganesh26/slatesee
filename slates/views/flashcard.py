from slates.models import FlashCard, User
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from slates.serializer import FlashCardSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class FlashCardList(APIView):
    """
    List all flashcards, or create a new flashcard.
    """
    def get(self, request, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        page = int(request.query_params.get('page', 1))
        page_size = 6
        if request.user.user_type=='student':
            flashcard_list = FlashCard.objects.filter( is_approved=1, 
                created_by=request.user.teacher_id)
        elif (request.user.user_type=='teacher' or request.user.user_type=='principal'):
            appr = request.query_params.get('is_approved', 0)
            if request.user.user_type=='teacher':
                creators = [request.user.id]
            if request.user.user_type=='principal':
                creators = [u.id for u in User.objects.filter(teacher_id=request.user.id)]
                creators.append(request.user.id)
            flashcard_list = FlashCard.objects.filter(is_approved=appr, created_by__in=creators)
        paginator = Paginator(flashcard_list, page_size)
        try:
            flashcards = paginator.page(page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            flashcards = paginator.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            flashcards = paginator.page(paginator.num_pages)
        serializer = FlashCardSerializer(flashcards, many=True)
        response_data = serializer.data
        if flashcards:
            response_data = serializer.data+[{"user_type":request.user.user_type}]
        return Response(response_data)

    def post(self, request, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if request.user.user_type not in ["teacher", "principal"]:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if 'created_by' not in request.data:
            request.data['created_by'] = request.user.id
        if 'updated_by' not in request.data:
            request.data['updated_by'] = request.user.id
        serializer = FlashCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        flashcard = self.get_object(pk)
        flashcard.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FlashCardDetail(APIView):
    """
    Retrieve, update or delete a flashcard instance.
    """
    def get_object(self, pk):
        try:
            return FlashCard.objects.get(pk=pk)
        except FlashCard.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        flashcard = self.get_object(pk)
        flashcard = FlashCardSerializer(flashcard)
        return Response(flashcard.data)

    def get_all_data(self, rdata, flashcard):
        data = {k:v for k, v in rdata.items()}
        if not rdata.get('side_a'):
            data['side_a'] = flashcard.side_a
        if not data.get('side_b'):
            data['side_b'] = flashcard.side_b
        return data

    def put(self, request, pk, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        flashcard = self.get_object(pk)
        data = self.get_all_data(request.data, flashcard)
        serializer = FlashCardSerializer(flashcard, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if not request.user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        flashcard = self.get_object(pk)
        flashcard.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)