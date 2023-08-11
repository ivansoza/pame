from django.shortcuts import render

from .models import Extranjero, PuestaDisposicionAC, PuestaDisposicionINM
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView
from .forms import extranjeroFormsAC, extranjeroFormsInm, puestDisposicionINMForm, puestaDisposicionACForm







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


class inicioACList(ListView):
    model = PuestaDisposicionAC
    template_name = "home/puestas/homePuestaAC.html" 
    context_object_name = 'puestaAC'

class createPuestaINM(CreateView):
    model = PuestaDisposicionINM               
    form_class = puestDisposicionINMForm      
    template_name = 'home/puestas/createPuestaINM.html'  
    success_url = reverse_lazy('homePuestaINM')


class createPuestaAC(CreateView):
    model = PuestaDisposicionAC
    form_class = puestaDisposicionACForm
    template_name = 'home/puestas/createPuestaAC.html'  
    success_url = reverse_lazy('homePuestaAC')



class createExtranjeroINM(CreateView):
    model =Extranjero             
    form_class = extranjeroFormsInm    
    template_name = 'home/puestas/crearExtranjeroINM.html' 
    success_url = reverse_lazy('homePuestaINM')

    def get_initial(self):
        initial = super().get_initial()
        initial['deLaPuestaIMN'] = self.kwargs['puesta_id']
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['puesta_id'] = self.kwargs['puesta_id']
        return context
    

    # def get_success_url(self):
    #     return f'//{self.kwargs["puesta_id"]}/'



class createExtranjeroAC(CreateView):
    model =Extranjero             
    form_class = extranjeroFormsAC    
    template_name = 'home/puestas/createExtranjeroAC.html' 
    success_url = reverse_lazy('homePuestaAC')

    def get_initial(self):
        initial = super().get_initial()
        initial['deLaPuestaAC'] = self.kwargs['puesta_id']
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['puesta_id'] = self.kwargs['puesta_id']
        return context
class listarExtranjeros(ListView):
    model = Extranjero
    template_name = 'home/puestas/listExtranjenros.html'
    context_object_name = 'extranjeros'

    def get_queryset(self):
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionINM.objects.get(id=puesta_id)
        queryset = Extranjero.objects.filter(deLaPuestaIMN=puesta)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        puesta_id = self.kwargs['puesta_id']
        context['puesta'] = PuestaDisposicionINM.objects.get(id=puesta_id)
        return context
    