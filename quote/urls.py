from django.urls import path,include

from . import views

app_name = 'quote'

urlpatterns = [
    path('quote/', views.QuoteView.as_view(), name='quote_view'),
    path('quote/<int:pk>/', views.QuoteDetail.as_view(), name='quote_detail_view'),
  ]