from django.shortcuts import render

# Create your views here.


def homeMedicoGeneral(request):
    return render(request, "homeMedicoGeneral.html")



def homeMedicoResponsable(request):
    return render(request, "home/homeMedicoResponsable.html")

