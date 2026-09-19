from django.db import models


class Solicitud(models.Model):
    id_solicitud = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='usuario_id',
        related_name='solicitudes',
    )
    estado = models.ForeignKey(
        'catalogos.EstadoSolicitud',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='estado_id',
        related_name='solicitudes',
    )
    centro_salud_destino = models.ForeignKey(
        'infraestructura.CentroSalud',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='centro_salud_destino_id',
        related_name='solicitudes',
    )
    ambulancia = models.ForeignKey(
        'infraestructura.Ambulancia',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='ambulancia_id',
        related_name='solicitudes',
    )
    conductor = models.ForeignKey(
        'personal.DatosConductor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='conductor_id',
        related_name='solicitudes',
    )
    # Circular con Ruta a proposito: una solicitud dispara un incidente, que dispara una
    # ruta, que se referencia de vuelta aca una vez asignada. Nullable en las 3 tablas,
    # asi que makemigrations resuelve el ciclo solo (crea los 3 modelos y agrega esta FK
    # en una migracion aparte).
    ruta = models.ForeignKey(
        'despacho.Ruta',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='ruta_id',
        related_name='solicitudes',
    )
    fecha_hora = models.DateTimeField(null=True, blank=True)
    ubicacion_origen = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'solicitud'

    def __str__(self):
        return f'solicitud {self.pk}'


class Incidente(models.Model):
    id = models.AutoField(primary_key=True)
    solicitud = models.ForeignKey(
        Solicitud,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='solicitud_id',
        related_name='incidentes',
    )
    tipo = models.ForeignKey(
        'catalogos.TipoIncidente',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='tipo_id',
        related_name='incidentes',
    )
    prioridad = models.ForeignKey(
        'catalogos.Prioridad',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='prioridad_id',
        related_name='incidentes',
    )
    descripcion = models.TextField(null=True, blank=True)
    fecha_hora = models.DateTimeField(null=True, blank=True)
    ubicacion = models.CharField(max_length=255, null=True, blank=True)
    estado_incidente = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'incidente'

    def __str__(self):
        return f'incidente {self.pk}'


class Ruta(models.Model):
    id = models.AutoField(primary_key=True)
    incidente = models.ForeignKey(
        Incidente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='incidente_id',
        related_name='rutas',
    )
    ambulancia = models.ForeignKey(
        'infraestructura.Ambulancia',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='ambulancia_id',
        related_name='rutas',
    )
    conductor = models.ForeignKey(
        'personal.DatosConductor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='conductor_id',
        related_name='rutas',
    )
    centro_salud_destino = models.ForeignKey(
        'infraestructura.CentroSalud',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='centro_salud_destino_id',
        related_name='rutas',
    )
    origen = models.CharField(max_length=255, null=True, blank=True)
    destino = models.CharField(max_length=255, null=True, blank=True)
    distancia_km = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    tiempo_estimado = models.IntegerField(null=True, blank=True)
    tiempo_real = models.IntegerField(null=True, blank=True)
    fecha_hora_inicio = models.DateTimeField(null=True, blank=True)
    fecha_hora_fin = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'rutas'

    def __str__(self):
        return f'ruta {self.pk}'


class UsuarioIncidente(models.Model):
    """Tabla puente M:N. Usa id autoincremental + UniqueConstraint en vez de PK
    compuesta (mas simple que CompositePrimaryKey de Django 5.2+ para el equipo)."""
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.CASCADE,
        db_column='usuario_id',
        related_name='incidentes_asociados',
    )
    incidente = models.ForeignKey(
        Incidente,
        on_delete=models.CASCADE,
        db_column='incidente_id',
        related_name='usuarios_asociados',
    )

    class Meta:
        db_table = 'usuario_incidente'
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'incidente'], name='unique_usuario_incidente'),
        ]

    def __str__(self):
        return f'usuario {self.usuario_id} - incidente {self.incidente_id}'
