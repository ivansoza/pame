from django.urls import path, include

from .views import homeLLamadasTelefonicas, llamadasTelefonicas

urlpatterns = [
    # path('', homeLLamadasTelefonicas, name="homeLLamadasTelefonicas"),
    path('llamadas', llamadasTelefonicas.as_view(), name="llamadasTelefonicas"),
]
