from django.shortcuts import render
from django.views.generic import CreateView, ListView, TemplateView

# Create your views here.


def homeJuridicoGeneral(request):
    return render (request, "home/homeJuridicoGeneral.html")


def homeJuridico(request):
    return render (request, "/home/homeJuridico.html")

def homeJuridicoResponsable(request):
    return render (request, "home/homeJuridicoResponsable.html")

class notificacionDO(TemplateView):
    template_name ='home/notificacion_d_o.html'