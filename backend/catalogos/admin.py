from django.contrib import admin

from . import models

admin.site.register(models.Prioridad)
admin.site.register(models.EstadoSolicitud)
admin.site.register(models.EstadoTipoIncidente)
admin.site.register(models.TipoCentro)
admin.site.register(models.TipoAmbulancia)
admin.site.register(models.EstadoAmbulancia)
admin.site.register(models.TipoIncidente)
