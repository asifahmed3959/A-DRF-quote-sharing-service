import factory

from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken

from .models import Quote

User = get_user_model()


def get_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access" : str(refresh.access_token)
    }


class UserFactor(factory.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.Faker('user_name')