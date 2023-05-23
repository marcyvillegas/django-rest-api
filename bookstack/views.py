from django.http import JsonResponse
from .models import Book
from .serializers import BookSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def bookList(request):
    
    if request.method == 'GET':
        books = Book.objects.all() # get all the books
        serializer = BookSerializer(books, many=True) # serialize them
        return JsonResponse(serializer.data, safe=False) # return json
    
    if request.method == 'POST':
        serializer = BookSerializer(data=request.data) # bring it back as complex data
        if serializer.is_valid(): # if valid then save and return the data saved and http status
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

