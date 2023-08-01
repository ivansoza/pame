from django.shortcuts import render
from .forms import ResponsableForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Responsable


def home(request):
    return render(request,"index.html")


@login_required
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
