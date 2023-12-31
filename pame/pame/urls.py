"""
URL configuration for pame project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from catalogos import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('generales.urls')),

    path("catalogos/",include("catalogos.urls")),
    path("acuerdos/", include("acuerdos.urls")),
    path("actuaciones/", include("actuaciones.urls")),
    path("amparo/", include("amparo.urls")),
    path("certificado-medico/", include("certificadoMedico.urls")),
    path("comedor/", include("comedor.urls")),
    path("comparecencia/", include("comparecencia.urls")),
    path("consulado/", include("consulado.urls")),
    path("consulta-medica/", include("consultaMedica.urls")),
    path("farmacia/", include("farmacia.urls")),
    path("llamadas-telefonicas/", include("llamadasTelefonicas.urls")),
    path("pertenencias/", include("pertenencias.urls")),
    path("seguridad/", include("vigilancia.urls")),
    path("salud/", include("salud.urls")),
    path("juridico/", include("juridico.urls")),
    path("traslados/", include("traslados.urls")),
    path("biometricos/", include("biometricos.urls")),
    path("notificaciones/", include("notificaciones.urls")),
    path("alegatos/", include("alegatos.urls")),


]
