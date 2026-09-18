from django.contrib import admin
from django.urls import path, include

from usuarios.views_password import (
    RecuperarPasswordView,
    RecuperarEnviadoView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Rutas existentes del proyecto
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