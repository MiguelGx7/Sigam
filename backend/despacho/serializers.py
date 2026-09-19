from rest_framework import serializers


class SolicitudSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    usuario_id = serializers.IntegerField(required=False, allow_null=True)
    estado_id = serializers.IntegerField(required=False, allow_null=True)
    centro_salud_destino_id = serializers.IntegerField(required=False, allow_null=True)
    ambulancia_id = serializers.IntegerField(required=False, allow_null=True)
    conductor_id = serializers.IntegerField(required=False, allow_null=True)
    ruta_id = serializers.IntegerField(required=False, allow_null=True)
    fecha_hora = serializers.DateTimeField(required=False, allow_null=True)
    ubicacion_origen = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)


class IncidenteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    solicitud_id = serializers.IntegerField(required=False, allow_null=True)
    tipo_id = serializers.IntegerField(required=False, allow_null=True)
    prioridad_id = serializers.IntegerField(required=False, allow_null=True)
    descripcion = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    fecha_hora = serializers.DateTimeField(required=False, allow_null=True)
    ubicacion = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    estado_incidente = serializers.CharField(max_length=50, required=False, allow_null=True, allow_blank=True)


class RutaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    incidente_id = serializers.IntegerField(required=False, allow_null=True)
    ambulancia_id = serializers.IntegerField(required=False, allow_null=True)
    conductor_id = serializers.IntegerField(required=False, allow_null=True)
    centro_salud_destino_id = serializers.IntegerField(required=False, allow_null=True)
    origen = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    destino = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    distancia_km = serializers.DecimalField(max_digits=8, decimal_places=2, required=False, allow_null=True)
    tiempo_estimado = serializers.IntegerField(required=False, allow_null=True)
    tiempo_real = serializers.IntegerField(required=False, allow_null=True)
    fecha_hora_inicio = serializers.DateTimeField(required=False, allow_null=True)
    fecha_hora_fin = serializers.DateTimeField(required=False, allow_null=True)


class UsuarioIncidenteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    usuario_id = serializers.IntegerField()
    incidente_id = serializers.IntegerField()
