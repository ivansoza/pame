from django.urls import path, include
from django.contrib.auth.views import LoginView
from .views import CustomLoginView
from .views import home, menu, exit

urlpatterns = [
    path('', home, name="home"),
    path('menu/', menu, name='menu'),
    path('logout/', exit, name="exit"),
    path('login/', CustomLoginView.as_view(), name='login'),
]
