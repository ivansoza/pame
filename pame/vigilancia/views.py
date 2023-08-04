from django.forms.models import BaseModelForm
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import OficioPuestaDisposicionINMform, ExtranjeroForm, OficioPuestaDisposicionACform
from .models import OficioPuestaDisposicionINM, Extranjero, OficioPuestaDisposicionAC
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.views.generic import TemplateView, CreateView


# Create your views here.


def homeSeguridadGeneral(request):
    return render (request, "home/homeSeguridadGeneral.html")


def homeSeguridadResponsable(request):
    return render (request, "home/homeSeguridadResponsable.html")


def addAutoridadCompetente(request):
    return render(request, "addAutoridadCompetente.html")



def addHospedaje(request):
    return render(request, "addHospedaje.html")


def addTraslado(request):
    return render(request, "addTraslado.html")


class Puesta(TemplateView):
    template_name = 'addAccionMigratoria.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form1'] = OficioPuestaDisposicionINMform()
        context['form2'] = ExtranjeroForm()
        return context

class PuestaAutoridadCompetente(CreateView):
    model = OficioPuestaDisposicionAC
    fields = '__all__'
    model2 = Extranjero
    fields2 = '__all__'
    template_name = 'addAutoridadCompetente.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form4'] = OficioPuestaDisposicionACform()
        context['form2'] = ExtranjeroForm()
        return context

# Primera vista funcional 
# class Puesta(CreateView):
#     model = OficioPuestaDisposicionINM
#     form_class = OficioPuestaDisposicionINMform
#     template_name = 'addAccionMigratoria.html'
#     success_url = '/'

#     def form_valid(self, form ):
#         messages.success(self.request, "Registro Exitoso")
#         return super().form_valid(form)
    
# class FormularioUno(forms.Form):
#     model = OficioPuestaDisposicionINM
#     form_class = OficioPuestaDisposicionINMform

# class FormularioDos(forms.Form):
#     model = Extranjero
#     forms_class = ExtranjeroForm

# class Puesta(CreateView):
#     template_name = 'addAccionMigratoria.html'
#     model = OficioPuestaDisposicionINM
#     form_class = OficioPuestaDisposicionINMform

#     def get_queryset(self):
#         return ExtranjeroForm.objetcs.all()

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form2'] = FormularioDos()
#         return context
    
#     def post(self, request, *args, **kwargs):
#         form1 = FormularioUno(request.POST)
#         form2 = FormularioDos(request.POST)

#         if form1.is_valid() and form2.is_valid():
#             OficioPuestaDisposicionINM_instance = form1.save()
#             Extranjero_instance = form2.save()

#             return self.form_valid(form1)
#         else:
#             return self.form_invalid(form1)

# class Puesta(CreateView):
#     template_name = 'addAccionMigratoria.html'
#     form_class_one = OficioPuestaDisposicionINMform
#     form_class_two = ExtranjeroForm
#     model = OficioPuestaDisposicionINM, Extranjero
#     # form_class = OficioPuestaDisposicionINMform, ExtranjeroForm
#     success_url = '/'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form_one'] = self.form_class_one()
#         context['form_two'] = self.form_class_two()
#         return context

    # def form_valid(self, form):
    #     extranjero_form = ExtranjeroForm(self.request.POST)
    #     if form.is_valid() and extranjero_form.is_valid():
    #         self.object = form.save()
    #         extranjero = extranjero_form.save(commit=False)
    #         extranjero.oficio_puesta = self.object
    #         extranjero.save()
    #         messages.success(self.request, "Registro Exitoso")
    #         return super().form_valid(form)
    #     else:
    #         return self.form_invalid(form)

