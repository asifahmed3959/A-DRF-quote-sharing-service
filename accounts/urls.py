from django.urls import path,include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
TokenVerifyView
)

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/',views.user_registration,name='registration'),
path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name='token_blacklisted'),

    ]