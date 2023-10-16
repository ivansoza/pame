from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView
# Create your views here.
from .models import ImagenCarrousel


def home(request):
    carrousels = ImagenCarrousel.objects.all()
    context = {"carrousels":carrousels}
    return render(request,'home2.html', context)

def menu(request):
    return render(request, 'menu.html',{'navbar':'home'})


def menuDefensoria(request):
    return render(request, 'menuDefensoria.html',{'navbar':'home'})


def exit(request):
    logout(request)
    return redirect('home')


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_invalid(self, form):
         mostrarAlerta = True
         return render(self.request, 'registration/login.html', {'mostrarAlerta': mostrarAlerta})

    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name='MedicoResponsable').exists():
            return reverse_lazy('menu')
        
        elif user.groups.filter(name='MedicoGeneral').exists():
            return reverse_lazy('menu')
        
        elif user.groups.filter(name='CocinaResponsable').exists():
            return reverse_lazy('menu')
        
        elif user.groups.filter(name='CocinaGeneral').exists():
            return reverse_lazy('menu')
        
        elif user.groups.filter(name='SeguridadResponsable').exists():
            return reverse_lazy('menu')
        
        elif user.groups.filter(name='SeguridadGeneral').exists():
            return reverse_lazy('menu')
        elif user.groups.filter(name='Administradores').exists():
            return reverse_lazy('menu')
        elif user.groups.filter(name='JuridicoGeneral').exists():
            return reverse_lazy('menu')
        elif user.groups.filter(name='JuridicoResponsable').exists():
            return reverse_lazy('menu')
        else:
            return reverse_lazy('home')
        
class DefensoriaLoginView(LoginView):
    template_name = 'registration/loginDefenseria.html'

    # Implementa el comportamiento específico para este tipo de login aquí
    def form_invalid(self, form):
         mostrarAlerta = True
         return render(self.request, 'registration/loginDefenseria.html', {'mostrarAlerta': mostrarAlerta})
    def get_success_url(self):
            user = self.request.user
            if user.groups.filter(name='MedicoResponsable').exists():
                return reverse_lazy('menuDefensoria')
            
            elif user.groups.filter(name='MedicoGeneral').exists():
                return reverse_lazy('menuDefensoria')
            
            elif user.groups.filter(name='CocinaResponsable').exists():
                return reverse_lazy('menuDefensoria')
            
            elif user.groups.filter(name='CocinaGeneral').exists():
                return reverse_lazy('menuDefensoria')
            
            elif user.groups.filter(name='SeguridadResponsable').exists():
                return reverse_lazy('menuDefensoria')
            
            elif user.groups.filter(name='SeguridadGeneral').exists():
                return reverse_lazy('menuDefensoria')
            elif user.groups.filter(name='Administradores').exists():
                return reverse_lazy('menuDefensoria')
            elif user.groups.filter(name='JuridicoGeneral').exists():
                return reverse_lazy('menuDefensoria')
            elif user.groups.filter(name='JuridicoResponsable').exists():
                return reverse_lazy('menuDefensoria')
            else:
                return reverse_lazy('home')




class templeteDenegado(TemplateView):
    template_name = 'permisoDenegado.html'