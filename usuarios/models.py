from django.contrib.auth.models import AbstractUser
from django.db import models


class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'roles'

    def __str__(self):
        return self.nombre


class Usuario(AbstractUser):
    nombre = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, unique=True)
    rol = models.ForeignKey(
        Rol,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios'
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return self.nombre