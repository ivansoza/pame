from django.urls import path, include
from .import views
from .views import defensoria,notificar,tabladefensores,SubirArchivo,modalnotificar, listExtranjerosComar, listExtranjerosConsulado, listExtranjerosFiscalia


urlpatterns = [
    path('defensoria', defensoria.as_view(), name="defensoria"),
    path('defensores', views.defensores, name='defensores'),
    path('notificacion/<int:pk>/', notificar.as_view(), name='notificacion'),
    path('listdefensores/', tabladefensores.as_view(), name='listdefensores'),
    path('modal/', SubirArchivo.as_view(), name='modale'),
    path('listnotificacion/<int:extranjero_id>/<int:defensoria_id>/', modalnotificar.as_view(), name='listnotificacion'),
    # Notificaciones
    path("comar/", listExtranjerosComar.as_view(), name="listExtranjerosComar"),
    path("consulado/", listExtranjerosConsulado.as_view(), name="listExtranjerosConsulado"),
    path("fiscalia/", listExtranjerosFiscalia.as_view(), name="listExtranjerosFiscalia"),


]
