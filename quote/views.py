from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import Http404
from django.forms.models import model_to_dict

from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.decorators import APIView, api_view,permission_classes
from rest_framework import permissions
from rest_framework.views import APIView

from .serializers import QuoteListSerializer
from .serializers import QuoteSaveSerializer
from .serializers import QuoteUpdateSerializer

from .models import Quote

from .permissions import IsOwnerOrReadOnly


User = get_user_model()


class QuoteView(APIView):
    """
    List all quotes by either username or any text of the quote, or create a quote.
    """
    permission_classes = ([permissions.IsAuthenticated,])

    def get(self, request, format=None):

        if "username" in request.data:
            username = request.data['username']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            quote = Quote.objects.filter(author=user.id)
            serializer = QuoteListSerializer(quote, many=True)
            return Response(serializer.data)

        elif "text" in request.data:
            text = request.data['text']
            try:
                quote = Quote.objects.filter(quote__icontains=text)
            except Quote.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = QuoteListSerializer(quote, many=True)
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

    def post(self, request, format=None):

        if "quote" in request.data and "author" not in request.data:
            quote = request.data['quote']
            object = Quote(quote=quote, author = request.user)
            serializer = QuoteSaveSerializer(data=model_to_dict(object))

        else:
            serializer = QuoteSaveSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuoteDetail(GenericAPIView):
    """
    Retrieve, update or delete a quote instance.
    """
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)

    def get_object(self, pk):
        try:
            return Quote.objects.get(pk=pk)
        except Quote.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        quote = self.get_object(pk)
        self.check_object_permissions(request, quote)
        serializer = QuoteListSerializer(quote)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        quote = self.get_object(pk)
        serializer = QuoteUpdateSerializer(quote, data=request.data)
        self.check_object_permissions(request, quote)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        quote = self.get_object(pk)
        self.check_object_permissions(request, quote)
        quote.delete()
        return Response({"quote": "deleted"},status=status.HTTP_204_NO_CONTENT)

