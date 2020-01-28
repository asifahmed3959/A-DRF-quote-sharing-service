from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.decorators import APIView, permission_classes
from rest_framework import permissions
from rest_framework.decorators import api_view

from .serializers import RefreshTokenSerializer
from accounts.serializers import UserSerializer

User = get_user_model()

@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny,])
def user_registration(request):
    """
    List all required docs, or create a new user.
    """
    if request.method == 'GET':
        serializer = UserSerializer()
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response({"logout":"validated"})