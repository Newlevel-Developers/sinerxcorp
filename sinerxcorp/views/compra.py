from django.shortcuts import render

def compra(request):
    return render(request, 'page/compra.html')

def ver_cursos(request):
    return render(request, 'page/ver_curso.html')

