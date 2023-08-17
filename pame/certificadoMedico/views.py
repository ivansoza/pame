
from django.shortcuts import render, redirect
from .forms import PuestaGeneralForm, Complemento1Form, Complemento2Form
from .models import PuestaGeneral


# def homeCertificadoMedico(request):
#     complemento1_form = Complemento1Form()
#     complemento2_form = Complemento2Form()
    
#     if request.method == 'POST':
#         puesta_general_form = PuestaGeneralForm(request.POST)
#         complemento_selector = request.POST.get('complemento_selector')
        
#         if puesta_general_form.is_valid():
#             puesta_general = puesta_general_form.save()
            
#             print(f"Complemento selector: {complemento_selector}")  # Añadido para depuración
            
#             if complemento_selector == 'complemento1':
#                 print("Guardando Complemento 1...")  # Añadido para depuración
#                 complemento_form = Complemento1Form(request.POST)
#                 if complemento_form.is_valid():
#                     complemento = complemento_form.save(commit=False)
#                     complemento.puesta_general = puesta_general
#                     complemento.save()
#                     print("Complemento 1 guardado exitosamente!")  # Añadido para depuración
#                 else:
#                     print("Formulario de Complemento 1 no válido!")  # Añadido para depuración
#             elif complemento_selector == 'complemento2':
#                 print("Guardando Complemento 2...")  # Añadido para depuración
#                 complemento_form = Complemento2Form(request.POST)
#                 if complemento_form.is_valid():
#                     complemento = complemento_form.save(commit=False)
#                     complemento.puesta_general = puesta_general
#                     complemento.save()
#                     print("Complemento 2 guardado exitosamente!")  # Añadido para depuración
#                 else:
#                     print("Formulario de Complemento 2 no válido!")  # Añadido para depuración
                    
#             return redirect('homeCertificadoMedico')
#     else:
#         puesta_general_form = PuestaGeneralForm()
    
#     return render(request, 'homeCertificadoMedico.html', {
#         'puesta_general_form': puesta_general_form,
#         'complemento1_form': complemento1_form,
#         'complemento2_form': complemento2_form,
#     })

def homeCertificadoMedico(request):
    if request.method == 'POST':
        print("Entrando al bloque POST")
        puesta_general_form = PuestaGeneralForm(request.POST)
        complemento_selector = request.POST.get('complemento_selector')
        
        if puesta_general_form.is_valid():
            print("Formulario de Puesta General válido")
            puesta_general = puesta_general_form.save()
            
            if complemento_selector == 'complemento1':
                print("Seleccionado Complemento1")
                complemento_form = Complemento1Form(request.POST)
                if complemento_form.is_valid():
                    print("Formulario de Complemento1 válido")
                    complemento = complemento_form.save(commit=False)
                    complemento.puesta_general = puesta_general
                    complemento.save()
            elif complemento_selector == 'complemento2':
                print("Seleccionado Complemento2")
                complemento_form = Complemento2Form(request.POST)
                if complemento_form.is_valid():
                    print("Formulario de Complemento2 válido")
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



# def homeCertificadoMedico(request):
#     if request.method == 'POST':
#         form = Puesta1Form(request.POST)  # Inicializamos el formulario con los datos comunes

#         if 'puestaType' in request.POST:  # Verificamos el tipo de puesta seleccionado
#             puesta_type = request.POST['puestaType']
#             if puesta_type == 'puesta1':
#                 form = Puesta1Form(request.POST)  # Si es Puesta 1, utilizamos el formulario Puesta1Form
#             elif puesta_type == 'puesta2':
#                 form = Puesta2Form(request.POST)  # Si es Puesta 2, utilizamos el formulario Puesta2Form

#             if form.is_valid():
#                 form.save()
#                 return redirect('ruta_de_redireccion')  # Redirige a donde quieras después de guardar
#     else:
#         form = Puesta1Form()

#     puesta1_form = Puesta1Form()
#     puesta2_form = Puesta2Form()

#     return render(request, 'homeCertificadoMedico.html', {'form': form, 'puesta1_form': puesta1_form, 'puesta2_form': puesta2_form})


# def homeCertificadoMedico(request):
#    return render(request,"homeCertificadoMedico.html")