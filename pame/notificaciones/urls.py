from django.urls import path, include
from .views import editarDefensoria 
from .views import defensoria,notificar,tabladefensores,SubirArchivo,modalnotificar, listExtranjerosComar, listExtranjerosConsulado, listExtranjerosFiscalia, createDEfensoria


urlpatterns = [
    path('defensoria', defensoria.as_view(), name="defensoria"),
    path('notificacion/<int:pk>/', notificar.as_view(), name='notificacion'),
    path('listdefensores/', tabladefensores.as_view(), name='listdefensores'),
    path('modal/', SubirArchivo.as_view(), name='modale'),
    path('listnotificacion/<int:extranjero_id>/<int:defensoria_id>/', modalnotificar.as_view(), name='listnotificacion'),
    # Notificaciones
    path("comar/", listExtranjerosComar.as_view(), name="listExtranjerosComar"),
    path("consulado/", listExtranjerosConsulado.as_view(), name="listExtranjerosConsulado"),
    path("fiscalia/", listExtranjerosFiscalia.as_view(), name="listExtranjerosFiscalia"),

    path("crearDefensoria/", createDEfensoria.as_view(), name="crearDefensoria"),
    path("editarDefensoria/<int:pk>", editarDefensoria.as_view(), name="editarDefensoria"),

]
