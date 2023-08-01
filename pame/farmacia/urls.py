from django.urls import path, include

from .views import homeFarmacia

urlpatterns = [
    path('', homeFarmacia, name="homeFarmacia"),


    

    
]
