from django.shortcuts import render

from .models import Extranjero, PuestaDisposicionAC, PuestaDisposicionINM
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView








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

def homePuestaINM (request):
    return render(request, "home/puestas/homePuestaINM.html")

def homePuestaVP (request):
    return render(request, "home/puestas/homePuestaVP.html")

class inicioINMList(ListView):
    model = PuestaDisposicionINM          
    template_name = "home/puestas/homePuestaINM.html" 
    context_object_name = 'puestasinm'

class createPuestaINM(CreateView):
    model = PuestaDisposicionINM               
    form_class = puestDisposicionINMForm      
    template_name = 'home/puestas/createPuestaINM.html'  
    success_url = reverse_lazy('homePuestaINM')

class createExtranjeroINM(CreateView):
    model =Extranjero             
    form_class = extranjeroFormsInm    
    template_name = 'home/puestas/crearExtranjeroINM.html'  
    success_url = reverse_lazy('homePuestaINM')