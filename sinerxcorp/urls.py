from django.urls import path
from sinerxcorp import views

urlpatterns = [
    path('', views.index, name='index')
]
