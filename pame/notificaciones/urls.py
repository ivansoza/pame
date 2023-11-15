from django.urls import path, include
from .import views
from .views import defensoria


urlpatterns = [
    path('defensoria', defensoria.as_view(), name="defensoria"),
    path('defensores', views.defensores, name='defensores'),
]