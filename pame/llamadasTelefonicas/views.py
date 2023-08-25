from django.shortcuts import render
from django.views import View
from .models import llamadasTelefonicas
from vigilancia.models import Extranjero

def homeLLamadasTelefonicas(request):
    return render(request,"LtIMN/LtIMN.html")

class llamadasTelefonicas(View):
    template_name = 'LtIMN/LtIMN.html'

    def get(self, request):
        extranjero = Extranjero.objects.first()
        estancia = Extranjero.objects.first()

        nombre_extranjero = extranjero.nombreExtranjero
        estancia_extranjero = estancia.deLaEstacion

        context = {
            'nombre_extranjero': nombre_extranjero,
            'estancia_extranjero': estancia_extranjero
        }
        return render(request, self.template_name, context)
