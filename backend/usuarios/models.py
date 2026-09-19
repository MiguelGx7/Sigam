from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'roles'

    def __str__(self):
        return self.nombre


class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un email')
        email = self.normalize_email(email)
        usuario = self.model(email=email, nombre=nombre, **extra_fields)
        usuario.set_password(password)  # esto hashea la contraseña
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, nombre, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, nombre, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, unique=True)
    rol = models.ForeignKey(
        Rol,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios'
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return self.nombre


class SolicitudCambioPassword(models.Model):
    """Notificación interna generada cuando un usuario pide recuperar su contraseña."""
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='solicitudes_password')
    creada_en = models.DateTimeField(auto_now_add=True)
    atendida = models.BooleanField(default=False)
    atendida_en = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'solicitudes_cambio_password'
        ordering = ['-creada_en']

    def __str__(self):
        return f'Solicitud de {self.usuario.email}'
