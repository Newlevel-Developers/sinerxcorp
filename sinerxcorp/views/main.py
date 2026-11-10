from django.shortcuts import render

def index(request):
    return render(request, 'page/index.html')

def login_views(request):
    return render(request, 'page/login.html')

def register(request):
    return render(request, 'page/registrar_usuarios.html')

def dashboard(request):
    return render(request, 'page/dashboard.html')