from django.urls import path,include

from . import views

app_name = 'quote'

urlpatterns = [
    path('home/', views.quote_view, name='quote_view'),

    ]