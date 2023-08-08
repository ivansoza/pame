from django.urls import path, include
from django.contrib.auth.views import LoginView
from .views import CustomLoginView
from .views import home, menu, exit
from django.contrib.auth import views as auth_views


from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', home, name="home"),
    path('menu/', menu, name='menu'),
    path('logout/', exit, name="exit"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('recuperar-contrasena/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('recuperar-contrasena/hecho/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('recuperar-contrasena/confirmar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('recuperar-contrasena/completado/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)