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
        serializer = BookSerializer(books, many=True) # serialize them / convert into JSON
        return JsonResponse(serializer.data, safe=False) # return json
    
    if request.method == 'POST':
        serializer = BookSerializer(data=request.data) # bring it back as complex data
        if serializer.is_valid(): # if valid then save and return the data saved and http status
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def bookDetail(request, id):
    
    try:
        book = Book.objects.get(pk=id)
    except Book.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = BookSerializer(book)
        return JsonResponse(serializer.data)
    
    if request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)