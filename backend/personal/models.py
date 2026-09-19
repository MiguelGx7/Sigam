from django.db import models


class DatosConductor(models.Model):
    id_conductor = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='usuario_id',
        related_name='datos_conductor',
    )
    licencia = models.CharField(max_length=50, null=True, blank=True)
    categoria_licencia = models.CharField(max_length=10, null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    centro_salud = models.ForeignKey(
        'infraestructura.CentroSalud',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='centro_salud_id',
        related_name='conductores',
    )
    estado = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'datos_conductor'

    def __str__(self):
        return self.licencia or f'conductor {self.pk}'


class Turno(models.Model):
    id_turno = models.AutoField(primary_key=True)
    conductor = models.ForeignKey(
        DatosConductor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='conductor_id',
        related_name='turnos',
    )
    ambulancia = models.ForeignKey(
        'infraestructura.Ambulancia',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='ambulancia_id',
        related_name='turnos',
    )
    fecha = models.DateField(null=True, blank=True)
    hora_inicio = models.TimeField(null=True, blank=True)
    hora_fin = models.TimeField(null=True, blank=True)
    estado_turno = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'turnos'

    def __str__(self):
        return f'turno {self.pk}'
