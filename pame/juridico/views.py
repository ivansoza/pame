from django.shortcuts import render

# Create your views here.


def homeJuridicoGeneral(request):
    return render (request, "home/homeJuridicoGeneral.html")


def homeJuridico(request):
    return render (request, "/home/homeJuridico.html")

def homeJuridicoResponsable(request):
    return render (request, "home/homeJuridicoResponsable.html")