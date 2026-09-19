from rest_framework import serializers


class DatosConductorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    usuario_id = serializers.IntegerField(required=False, allow_null=True)
    licencia = serializers.CharField(max_length=50, required=False, allow_null=True, allow_blank=True)
    categoria_licencia = serializers.CharField(max_length=10, required=False, allow_null=True, allow_blank=True)
    fecha_vencimiento = serializers.DateField(required=False, allow_null=True)
    centro_salud_id = serializers.IntegerField(required=False, allow_null=True)
    estado = serializers.CharField(max_length=50, required=False, allow_null=True, allow_blank=True)


class TurnoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    conductor_id = serializers.IntegerField(required=False, allow_null=True)
    ambulancia_id = serializers.IntegerField(required=False, allow_null=True)
    fecha = serializers.DateField(required=False, allow_null=True)
    hora_inicio = serializers.TimeField(required=False, allow_null=True)
    hora_fin = serializers.TimeField(required=False, allow_null=True)
    estado_turno = serializers.CharField(max_length=50, required=False, allow_null=True, allow_blank=True)
