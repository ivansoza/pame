from django.urls import path, include

from .views import home, menu, exit

urlpatterns = [
    path('', home, name="home"),
    path('menu/', menu, name='menu'),
    path('logout/', exit, name="exit")
    
]
