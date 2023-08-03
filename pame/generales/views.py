from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
# Create your views here.



def home(request):
    return render(request,'home.html')

def menu(request):
    return render(request, 'menu.html')


def exit(request):
    logout(request)
    return redirect('home')


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name='MedicoResponsable').exists():
            return reverse_lazy('homeMedicoResponsable')
        elif user.groups.filter(name='MedicoGeneral').exists():
            return reverse_lazy('homeMedicoGeneral')
        elif user.groups.filter(name='CocinaResponsable').exists():
            return reverse_lazy('homeComedor')
        elif user.groups.filter(name='CocinaGeneral').exists():
            return reverse_lazy('homeComedor')
        elif user.groups.filter(name='SeguridadResponsable').exists():
            return reverse_lazy('homeSeguridadResponsable')
        elif user.groups.filter(name='SeguridadGeneral').exists():
            return reverse_lazy('homeSeguridadGeneral')
        elif user.groups.filter(name='admin').exists():
            return reverse_lazy('menu')
        elif user.groups.filter(name='JuridicoGeneral').exists():
            return reverse_lazy('homeJuridicoGeneral')
        elif user.groups.filter(name='JuridicoResponsable').exists():
            return reverse_lazy('homeJuridicoResponsable')
        elif user.groups.filter(name='admin').exists():
            return reverse_lazy('menu')
        else:
            return reverse_lazy('home')


