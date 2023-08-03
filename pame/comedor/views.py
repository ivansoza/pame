from django.shortcuts import render

# Create your views here.


def homeCocinaGeneral (request):
    return render(request, "homeCocinaGeneral.html")

def homeCocinaResponsable (request):
    return render(request, "homeCocinaResponsable.html")
