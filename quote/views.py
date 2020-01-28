from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.decorators import APIView, api_view,permission_classes
from rest_framework import permissions

from .serializers import QuoteListSerializer
from .serializers import QuoteSaveSerializer

from .models import Quote

User = get_user_model()

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly,])
def quote_view(request):
    """
    List all user required data, or create a user.
    """
    if request.method == 'GET':
        quote = Quote.objects.all()
        serializer = QuoteListSerializer(quote,many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = QuoteSaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)