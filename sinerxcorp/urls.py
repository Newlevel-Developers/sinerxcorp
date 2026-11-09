from django.urls import path
from sinerxcorp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('login_user/', views.login_user, name='login_user'),
    path('register/', views.register, name='register'),
    path('compra/', views.compra, name='compra'),
    path('ver_cursos/', views.ver_cursos, name='ver_cursos'),
    path('method_payment/', views.payment, name='method_payment')
]
