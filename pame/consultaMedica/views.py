from django.shortcuts import render

# Create your views here.


def homeConsultaMedica(request):
    return render(request,"homeConsultaMedica.html")
