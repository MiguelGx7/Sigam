from django.db import models

class Usuario(models.Model):
    ROLES = [
        ('Personal', 'Personal'),
        ('Operador', 'Operador'),
        ('Administrador', 'Administrador'),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    documento = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(unique=True)
    rol = models.CharField(max_length=50, choices=ROLES)
    password = models.CharField(max_length=128)
    acepta_terminos = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"