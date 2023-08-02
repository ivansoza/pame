from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import OficioPuestaDisposicionINMform
from .models import OficioPuestaDisposicionINM
from django.urls import reverse_lazy
# Create your views here.


def homeSeguridadGeneral(request):
    return render (request, "homeSeguridadGeneral.html")


def addAutoridadCompetente(request):
    return render(request, "addAutoridadCompetente.html")



def addHospedaje(request):
    return render(request, "addHospedaje.html")


def addTraslado(request):
    return render(request, "addTraslado.html")


class Puesta(CreateView):
    model = OficioPuestaDisposicionINM
    form_class = OficioPuestaDisposicionINMform
    template_name = 'addAccionMigratoria.html'