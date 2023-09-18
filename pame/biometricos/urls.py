from django.urls import path, include

from .views import scanner

urlpatterns = [
    path('scanner', scanner, name="scanner"),

    
]
