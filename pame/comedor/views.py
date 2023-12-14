from django.shortcuts import render
from django.views import View
from vigilancia.models import Extranjero, NoProceso
from salud.models import TIPO_DIETAS, CertificadoMedico
from django.contrib.auth.mixins import LoginRequiredMixin
from vigilancia.views import ListView
from django.db.models import Max
from django.db.models import Exists, OuterRef, Subquery


def homeCocinaGeneral (request):
    return render(request, "home/homeCocinaGeneral.html")

def homeCocinaResponsable (request):
    return render(request, "home/homeCocinaResponsable.html")
class comedor(LoginRequiredMixin, ListView):
    model = NoProceso
    template_name='home/comedor.html'
    context_object_name = 'extranjeros'
    login_url = '/permisoDenegado/'
    

    def get_queryset(self):
        estacion_usuario = self.request.user.estancia
        tipo_dieta = self.request.GET.get('tipo_dieta', None)

        # Filtrar extranjeros por estación
        extranjeros_filtrados = Extranjero.objects.filter(deLaEstacion=estacion_usuario)

        # Filtrar por el último NoProceso para cada extranjero
        ultimo_no_proceso = NoProceso.objects.filter(
            extranjero_id=OuterRef('pk')
        ).order_by('-consecutivo')

        extranjeros_filtrados = extranjeros_filtrados.annotate(
            ultimo_nup_id=Subquery(ultimo_no_proceso.values('nup')[:1])
        )

        # Obtener todos los NoProceso que tengan al menos un CertificadoMedico
        queryset = NoProceso.objects.filter(
            nup__in=[e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id],
            certificados_medicos__isnull=False
        ).distinct()



        # Aplicar el filtro de tipo de dieta
        
        if tipo_dieta == 'general':
            queryset = queryset.filter(certificados_medicos__tipoDieta='GENERAL')
        elif tipo_dieta == 'religiosa':
            queryset = queryset.filter(certificados_medicos__tipoDieta='RELIGIOSA')
        elif tipo_dieta == 'vegetariana':
            queryset = queryset.filter(certificados_medicos__tipoDieta='VEGETARIANA')
        elif tipo_dieta == 'clinica':
            queryset = queryset.filter(certificados_medicos__tipoDieta='CLÍNICA')

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['navbar'] = 'cocina'
        context['seccion'] = 'comedor'
        context['nombre_estacion'] = self.request.user.estancia.nombre
        context['tipo_dieta'] = CertificadoMedico.objects.values_list('tipoDieta', flat=True).distinct()

        return context
# class comedor(LoginRequiredMixin, ListView):
#     model = CertificadoMedico
#     template_name='home/comedor.html'
#     context_object_name = 'extranjeros'
#     login_url = '/permisoDenegado/'
    
#     def get_queryset(self):
#         estacion_usuario = self.request.user.estancia
#         estado = self.request.GET.get('estado_filtrado', 'activo')
#         tipo_dieta = self.request.GET.get('tipo_dieta', None)

#         extranjeros_filtrados = Extranjero.objects.filter(deLaEstacion=estacion_usuario)

#         if estado == 'activo':
#             extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Activo')
#         elif estado == 'inactivo':
#             extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Inactivo')

#         ultimo_no_proceso = NoProceso.objects.filter(
#             extranjero_id=OuterRef('pk')
#         ).order_by('-consecutivo')

#         extranjeros_filtrados = extranjeros_filtrados.annotate(
#             ultimo_nup_id=Subquery(ultimo_no_proceso.values('nup')[:1])
#         )

#         dietas = CertificadoMedico.objects.filter(
#             nup=OuterRef('pk'),
#             tipoDieta=tipo_dieta
#         )

#         queryset = NoProceso.objects.filter(
#             nup__in=[e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id]
#         ).annotate(
#             tiene_defensoria_asignada=Exists(dietas)
#         )

#         # Añade una anotación para obtener el ID de CertificadoMedico
#         queryset = queryset.annotate(
#             certificado_medico_id=Subquery(
#                 CertificadoMedico.objects.filter(nup=OuterRef('pk')).values('id')[:1]
#             )
#         )

#         if tipo_dieta:
#             queryset = queryset.filter(certificado_medico_id__isnull=False)
#         else:
#             queryset = queryset.filter(certificado_medico_id__isnull=True)

#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         context['navbar'] = 'cocina'
#         context['seccion'] = 'comedor'
#         context['nombre_estacion'] = self.request.user.estancia.nombre
#         context['tipo_dieta'] = CertificadoMedico.objects.values_list('tipoDieta', flat=True).distinct()

#         return context