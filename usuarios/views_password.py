from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


class RecuperarPasswordView(auth_views.PasswordResetView):
    template_name = "usuarios/recuperar.html"
    email_template_name = "registration/password_reset_email.html"
    success_url = reverse_lazy("recuperar_enviado")


class RecuperarEnviadoView(auth_views.PasswordResetDoneView):
    template_name = "usuarios/recuperar_enviado.html"


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "usuarios/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "usuarios/password_reset_complete.html"