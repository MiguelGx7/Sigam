from django.db import models


class CentroSalud(models.Model):
    id_centro = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    tipo_centro = models.ForeignKey(
        'catalogos.TipoCentro',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='tipo_centro_id',
        related_name='centros_salud',
    )

    class Meta:
        db_table = 'centros_salud'

    def __str__(self):
        return self.nombre


class Ambulancia(models.Model):
    id_ambulancia = models.AutoField(primary_key=True)
    placa = models.CharField(max_length=20)
    tipo = models.ForeignKey(
        'catalogos.TipoAmbulancia',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='tipo_id',
        related_name='ambulancias',
    )
    estado = models.ForeignKey(
        'catalogos.EstadoAmbulancia',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='estado_id',
        related_name='ambulancias',
    )
    centro_salud = models.ForeignKey(
        CentroSalud,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='centro_salud_id',
        related_name='ambulancias',
    )

    class Meta:
        db_table = 'ambulancias'

    def __str__(self):
        return self.placa
