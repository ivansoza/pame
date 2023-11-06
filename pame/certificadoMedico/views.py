
from django.shortcuts import render, redirect
from .forms import PuestaGeneralForm, Complemento1Form, Complemento2Form
from .models import PuestaGeneral


def homeCertificadoMedico(request):
    if request.method == 'POST':
        puesta_general_form = PuestaGeneralForm(request.POST)
        complemento_selector = request.POST.get('complemento_selector')
        
        if puesta_general_form.is_valid():
            puesta_general = puesta_general_form.save()
            
            if complemento_selector == 'complemento1':
                complemento_form = Complemento1Form(request.POST)
                if complemento_form.is_valid():
                    complemento = complemento_form.save(commit=False)
                    complemento.puesta_general = puesta_general
                    complemento.save()
            elif complemento_selector == 'complemento2':
                complemento_form = Complemento2Form(request.POST)
                if complemento_form.is_valid():
                    complemento = complemento_form.save(commit=False)
                    complemento.puesta_general = puesta_general
                    complemento.save()
                    
            return redirect('homeCertificadoMedico')
    else:
        puesta_general_form = PuestaGeneralForm()
        complemento1_form = Complemento1Form()
        complemento2_form = Complemento2Form()
    
    return render(request, 'homeCertificadoMedico.html', {
        'puesta_general_form': puesta_general_form,
        'complemento1_form': complemento1_form,
        'complemento2_form': complemento2_form,
    })

