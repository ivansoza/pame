from django.shortcuts import render

# Create your views here.

def homeMedico(request):
    return render(request, "home.html")


def homeMedicoGeneral(request):
    return render(request, "home/homeMedicoGeneral.html")



def homeMedicoResponsable(request):
    return render(request, "home/homeMedicoResponsable.html")

