from django.db import models


class Prioridad(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    nivel = models.CharField(max_length=50, null=True, blank=True)
    tiempo_respuesta_max = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'prioridad'

    def __str__(self):
        return self.nombre


class EstadoSolicitud(models.Model):
    """Catalogo de estados de una solicitud."""
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'estado'

    def __str__(self):
        return self.nombre


class EstadoTipoIncidente(models.Model):
    """Catalogo de estados de un tipo de incidente."""
    id_estado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'estados'

    def __str__(self):
        return self.nombre


class TipoCentro(models.Model):
    id_tipo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'tipos_centros'

    def __str__(self):
        return self.nombre


class TipoAmbulancia(models.Model):
    id_tipo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'tipos_ambulancia'

    def __str__(self):
        return self.nombre


class EstadoAmbulancia(models.Model):
    id_estado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'estados_ambulancia'

    def __str__(self):
        return self.nombre


class TipoIncidente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    estado = models.ForeignKey(
        EstadoTipoIncidente,
        on_delete=models.PROTECT,
        db_column='estados_id_estado',
        related_name='tipos_incidente',
    )

    class Meta:
        db_table = 'tipo_incidente'

    def __str__(self):
        return self.nombre
