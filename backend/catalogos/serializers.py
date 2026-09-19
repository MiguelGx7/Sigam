from rest_framework import serializers


class PrioridadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=100)
    nivel = serializers.CharField(max_length=50, required=False, allow_null=True)
    tiempo_respuesta_max = serializers.IntegerField(required=False, allow_null=True)


class EstadoSolicitudSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=100)
    descripcion = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class EstadoTipoIncidenteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=100)
    descripcion = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class TipoCentroSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=100)


class TipoAmbulanciaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=100)
    descripcion = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class EstadoAmbulanciaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=100)
    descripcion = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class TipoIncidenteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=100)
    estado_id = serializers.IntegerField()
    descripcion = serializers.CharField(required=False, allow_null=True, allow_blank=True)
