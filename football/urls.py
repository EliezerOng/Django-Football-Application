from django.urls import path
from . import views


app_name = 'football'
urlpatterns = [
    path('', views.football,name='football'),
]