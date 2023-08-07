from django.shortcuts import render
from django.views import View

# Create your views here.


def homeCocinaGeneral (request):
    return render(request, "home/homeCocinaGeneral.html")

def homeCocinaResponsable (request):
    return render(request, "home/homeCocinaResponsable.html")


