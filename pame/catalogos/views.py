from django.shortcuts import render
from .forms import ResponsableForm
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.
from .models import Responsable


def home(request):
    return render(request,"index.html")


def responsableCrear(request):
    form= ResponsableForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request,"Producto Agregado Exitosamente")
        return HttpResponseRedirect("/")
    context ={
        "form":form
    }
    return render(request,"addResponsable.html",context)
