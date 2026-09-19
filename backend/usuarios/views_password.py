from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SolicitudCambioPassword, Usuario

token_generator = PasswordResetTokenGenerator()

MENSAJE_GENERICO = 'Si el correo esta registrado, se enviaron instrucciones para recuperar la contraseña.'


class RecuperarPasswordView(APIView):
    """Paso 1: recibe un email, genera un token y lo 'envia' (backend de consola en dev)."""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '')
        usuario = Usuario.objects.filter(email=email).first()

        if usuario is not None:
            # La persona recibe su enlace y el Super Administrador ve una alerta en el panel.
            # get_or_create evita varias alertas pendientes por la misma cuenta.
            SolicitudCambioPassword.objects.get_or_create(usuario=usuario, atendida=False)
            uid = urlsafe_base64_encode(force_bytes(usuario.pk))
            token = token_generator.make_token(usuario)
            link = f'{settings.FRONTEND_URL}/recuperar/confirmar?uid={uid}&token={token}'
            send_mail(
                subject='Recuperacion de contraseña - SIGAM',
                message=f'Hola {usuario.nombre},\n\nPara restablecer tu contraseña entra a:\n{link}\n\nSi no fuiste tu, ignora este mensaje.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[usuario.email],
            )

        # Respuesta identica exista o no el usuario: no se revela si el email esta registrado.
        return Response({'mensaje': MENSAJE_GENERICO}, status=status.HTTP_200_OK)


class ConfirmarPasswordView(APIView):
    """Paso 2: recibe uid+token (del link) y la nueva contraseña."""
    permission_classes = [AllowAny]

    def post(self, request):
        uid = request.data.get('uid', '')
        token = request.data.get('token', '')
        nueva_password = request.data.get('nueva_password', '')

        if not nueva_password or len(nueva_password) < 6:
            return Response(
                {'error': 'La contraseña debe tener al menos 6 caracteres.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            usuario_id = force_str(urlsafe_base64_decode(uid))
            usuario = Usuario.objects.get(pk=usuario_id)
        except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
            usuario = None

        if usuario is None or not token_generator.check_token(usuario, token):
            return Response(
                {'error': 'El enlace de recuperacion es invalido o ya expiro.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        usuario.set_password(nueva_password)
        usuario.save()

        return Response({'mensaje': 'Contraseña actualizada correctamente.'}, status=status.HTTP_200_OK)
