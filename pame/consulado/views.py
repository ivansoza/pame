from django.shortcuts import render

# Create your views here.


def homeConsulado(request):
    return render(request,"homeConsulado.html")


