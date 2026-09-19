from rest_framework import serializers


class CentroSaludSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=150)
    direccion = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    telefono = serializers.CharField(max_length=20, required=False, allow_null=True, allow_blank=True)
    tipo_centro_id = serializers.IntegerField(required=False, allow_null=True)


class AmbulanciaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    placa = serializers.CharField(max_length=20)
    tipo_id = serializers.IntegerField(required=False, allow_null=True)
    estado_id = serializers.IntegerField(required=False, allow_null=True)
    centro_salud_id = serializers.IntegerField(required=False, allow_null=True)
