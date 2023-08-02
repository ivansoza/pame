from django.shortcuts import render

# Create your views here.


def homeSeguridadGeneral(request):
    return render (request, "homeSeguridadGeneral.html")


def addAutoridadCompetente(request):
    return render(request, "addAutoridadCompetente.html")


def addAccionMigratoria(request):
    return render(request, "addAccionMigratoria.html")

def addHospedaje(request):
    return render(request, "addHospedaje.html")


def addTraslado(request):
    return render(request, "addTraslado.html")
