from django.contrib import admin
<<<<<<< HEAD
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),
=======
from django.urls import path

from backend.usuarios.views import login_usuario, inicio
from backend.usuarios.views_password import (
    RecuperarPasswordView,
    RecuperarEnviadoView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Login e inicio
    path("login/", login_usuario, name="login"),
    path("inicio/", inicio, name="inicio"),

    # Recuperación de contraseña
    path(
        "recuperar/",
        RecuperarPasswordView.as_view(),
        name="recuperar",
    ),

    path(
        "recuperar/enviado/",
        RecuperarEnviadoView.as_view(),
        name="recuperar_enviado",
    ),

    path(
        "recuperar/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),

    path(
        "recuperar/completado/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
>>>>>>> 7f6292d (Implementa recuperación de contraseña)
]from django.contrib import admin
from django.urls import path, include

from usuarios.views_password import (
    RecuperarPasswordView,
    RecuperarEnviadoView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("usuarios.urls")),

    # Recuperación de contraseña
    path(
        "recuperar/",
        RecuperarPasswordView.as_view(),
        name="recuperar",
    ),
    path(
        "recuperar/enviado/",
        RecuperarEnviadoView.as_view(),
        name="recuperar_enviado",
    ),
    path(
        "recuperar/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "recuperar/completado/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]