from django.http import JsonResponse
from .models import Book
from .serializers import BookSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)


# User authentication - login, logout and signup
@api_view(["POST"])
def login(request):
    user = get_object_or_404(User, username=request.data["username"])

    if not user.check_password(request.data["password"]):
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    token = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})


@api_view(["POST"])
def logout(request):
    token = request.data.get("token")  # Get the user's token from the request data
    Token.objects.filter(key=token).delete()  # Delete the token from the database
    return Response({"message": "Logout successful"})


@api_view(["POST"])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        user = User.objects.get(username=request.data["username"])
        hashed_password = make_password(request.data["password"])
        user.set_password(hashed_password)
        user.save()

        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Book - this is a sample CRUD endpoint with token authentication
@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def bookList(request):
    if request.method == "GET":
        # get all the books
        books = Book.objects.all()

        # serialize them / convert into JSON
        serializer = BookSerializer(books, many=True)
        # return json
        return JsonResponse(serializer.data, safe=False)

    if request.method == "POST":
        # bring it back as complex data
        serializer = BookSerializer(data=request.data)

        # if valid then save and return the data saved and http status
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def bookDetail(request, id):
    try:
        book = Book.objects.get(pk=id)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = BookSerializer(book)
        return JsonResponse(serializer.data)

    if request.method == "PUT":
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
