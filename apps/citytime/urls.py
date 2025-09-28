from django.urls import path
from . import views

urlpatterns = [
    path('', views.city_time, name='city_time'),
]
