from django.urls import path,include
from .views import listaExtranjertoAlegatos, creaAlegato, subirDocumentosAlegatos, listaDocumentosAlegatos

urlpatterns = [
    path("listaExtranjerosAlegatos/", listaExtranjertoAlegatos.as_view(), name="listaExtranjerosAlegatos"),
    path("crearAlegato/<int:pk>/", creaAlegato.as_view(), name="crearAlegato"),
    path('documentosAlegato/<int:alegato_id>/', subirDocumentosAlegatos.as_view(), name='documentosAlegato'),
    path('documentosAlegatos/<int:pk>/', listaDocumentosAlegatos.as_view(), name='documentosAlegatos'),

]