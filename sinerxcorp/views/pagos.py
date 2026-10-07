from django.shortcuts import render

def payment(request):
    return render(request, 'page/metodo_pago.html')