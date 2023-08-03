from django.forms.models import BaseModelForm
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import OficioPuestaDisposicionINMform
from .models import OficioPuestaDisposicionINM
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.


def homeSeguridadGeneral(request):
    return render (request, "home/homeSeguridadGeneral.html")


def homeSeguridadResponsable(request):
    return render (request, "home/homeSeguridadResponsable.html")


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
    success_url = '/'

    def form_valid(self, form ):
        messages.success(self.request, "Registro Exitoso")
        return super().form_valid(form)
    

