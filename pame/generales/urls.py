from django.urls import path, include
from django.contrib.auth.views import LoginView
from .views import CustomLoginView, templeteDenegado, DefensoriaLoginView, menuDefensoria, firmaExistente
from .views import home, menu, exit
from django.contrib.auth import views as auth_views


from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', home, name="home"),
    path('menu/', menu, name='menu'),
    path('menu-defensoria/', menuDefensoria, name='menuDefensoria'),

    path('logout/', exit, name="exit"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('defensoria-login/', DefensoriaLoginView.as_view(), name='defensoriaLogin'),
    path('recuperar-contrasena/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('permisoDenegado/', templeteDenegado.as_view(), name='permisoDenegado'),
    path('recuperar-contrasena/hecho/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('recuperar-contrasena/confirmar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('recuperar-contrasena/completado/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('firma_existente/', firmaExistente.as_view(), name='firma_existente1'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)