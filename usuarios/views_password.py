from django.contrib import auth
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

import json


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


@csrf_exempt
def recuperar_password_api(request):

    if request.method != "POST":
        return JsonResponse(
            {
                "error": "Método no permitido."
            },
            status=405
        )

    try:
        data = json.loads(request.body)
        email = data.get("email", "").strip()

    except (json.JSONDecodeError, AttributeError):
        return JsonResponse(
            {
                "error": "Datos inválidos."
            },
            status=400
        )

    if not email:
        return JsonResponse(
            {
                "error": "El correo electrónico es obligatorio."
            },
            status=400
        )

    form = PasswordResetForm(
        {
            "email": email
        }
    )

    if form.is_valid():
        form.save(
            request=request,
            use_https=False
        )

    return JsonResponse(
        {
            "message": "Si el correo está registrado, recibirás un enlace para recuperar tu contraseña."
        },
        status=200
    )