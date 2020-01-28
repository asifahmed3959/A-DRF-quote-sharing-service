from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.decorators import APIView, api_view,permission_classes
from rest_framework import permissions

from .serializers import QuoteListSerializer
from .serializers import QuoteSaveSerializer
from .serializers import QuoteUpdateSerializer

from .models import Quote

User = get_user_model()

@api_view(['GET', 'POST','PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly,])
def quote_view(request):
    """
    List all quotes but either username or any text required data, or create a quote.
    """
    if request.method == 'GET':

        if "username" in request.data:
            username = request.data['username']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            quote = Quote.objects.filter(author=user.id)
            serializer = QuoteListSerializer(quote,many=True)
            return Response(serializer.data)

        elif "text" in request.data:
            text = request.data['text']
            try:
                quote = Quote.objects.filter(quote__icontains=text)
            except Quote.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = QuoteListSerializer(quote,many=True)
            return Response(serializer.data)

        elif "id" in request.data:

            id = request.data['id']
            try:
                quote = Quote.objects.get(pk=id)
            except Quote.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = QuoteListSerializer(quote)
            return Response(serializer.data)

        else:
            quote = Quote.objects.all()
            serializer = QuoteListSerializer(quote, many=True)
            return Response(serializer.data)


    elif request.method == 'POST':
        serializer = QuoteSaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated,])
def quote_detail(request):
    """
    Retrieve, update or delete a quote by its id.
    """
    id = request.data['id']

    try:
        quote = Quote.objects.get(pk=id)
    except Quote.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if quote.author == request.user:
        if request.method == 'GET':
            serializer = QuoteListSerializer(quote)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = QuoteUpdateSerializer(quote, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            quote.delete()
            return Response({"quote": "deleted"},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)






