from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import Quote

User = get_user_model()

class QuoteSaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quote
        fields = ['author','quote']

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','id']

class QuoteListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Quote
        fields = ['author','quote']