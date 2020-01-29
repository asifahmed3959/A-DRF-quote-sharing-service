from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.decorators import APIView, permission_classes
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView

from .serializers import BlackListRefreshTokenSerializer
from accounts.serializers import UserSerializer
from accounts.serializers import ChangePasswordSerializer


User = get_user_model()


class UserRegistation(CreateAPIView):
    """
    create a new user.
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class LogoutView(CreateAPIView):
    """
    blacklists the current refresh token, thus user cannnot use it to
    get access token.
    """
    serializer_class = BlackListRefreshTokenSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UpdatePassword(APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"password":"your password has been changed"},status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)