from django.contrib import admin

from . import models

admin.site.register(models.Solicitud)
admin.site.register(models.Incidente)
admin.site.register(models.Ruta)
admin.site.register(models.UsuarioIncidente)
