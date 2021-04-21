from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import Http404
from django.forms.models import model_to_dict

from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .serializers import QuoteListSerializer
from .serializers import QuoteSaveSerializer
from .serializers import QuoteUpdateSerializer

from .models import Quote

from .permissions import IsOwnerOrReadOnly


User = get_user_model()


class QuoteView(ListAPIView):
    """
    List all quotes by either username or any text of the quote, or create a quote.
    """
    permission_classes = ([permissions.IsAuthenticated,])
    serializer_class = QuoteListSerializer

    def get_queryset(self):

        queryset = Quote.objects.all()
        username = self.request.query_params.get('username', None)
        id = self.request.query_params.get('id', None)
        text = self.request.query_params.get('text')

        if username is not None:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            queryset = queryset.filter(author=user.id)
            return queryset

        elif id is not None:
            queryset = queryset.get(pk=id)
            return [queryset,]

        elif text is not None:
            queryset = queryset.filter(quote__icontains=text)
            return queryset

        else:
            return queryset


class CreateQuoteView(CreateAPIView):
    """
    create a new quote by the user
    """
    permission_classes =  ([permissions.IsAuthenticated,])
    serializer_class = QuoteSaveSerializer


class QuoteDetail(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a quote instance.
    """
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    serializer_class = QuoteUpdateSerializer
    queryset = Quote.objects.all()
