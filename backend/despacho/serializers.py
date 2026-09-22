from rest_framework import serializers

ESTADOS_INCIDENTE = [
    ('en_espera', 'En espera'),
    ('llegada_incidente_confirmada', 'Llegada al incidente confirmada'),
    ('observaciones_registradas', 'Observaciones registradas'),
    ('traslado_iniciado', 'Traslado iniciado'),
    ('hospital_seleccionado', 'Hospital seleccionado'),
    ('llegada_hospital_confirmada', 'Llegada al hospital confirmada'),
    ('cerrado', 'Cerrado'),
]

TRANSICIONES_VALIDAS = {
    'en_espera': {'llegada_incidente_confirmada'},
    'llegada_incidente_confirmada': {'observaciones_registradas'},
    'observaciones_registradas': {'traslado_iniciado'},
    'traslado_iniciado': {'hospital_seleccionado'},
    'hospital_seleccionado': {'llegada_hospital_confirmada'},
    'llegada_hospital_confirmada': {'cerrado'},
    'cerrado': set(),
}


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
    observaciones = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    fecha_hora = serializers.DateTimeField(required=False, allow_null=True)
    ubicacion = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    estado_incidente = serializers.ChoiceField(
        choices=[
            ('en_espera', 'En espera'),
            ('llegada_incidente_confirmada', 'Llegada al incidente confirmada'),
            ('observaciones_registradas', 'Observaciones registradas'),
            ('traslado_iniciado', 'Traslado iniciado'),
            ('hospital_seleccionado', 'Hospital seleccionado'),
            ('llegada_hospital_confirmada', 'Llegada al hospital confirmada'),
            ('cerrado', 'Cerrado'),
        ],
        required=False,
        allow_null=True,
    )


class IncidenteEstadoUpdateSerializer(serializers.Serializer):
    estado_incidente = serializers.ChoiceField(choices=ESTADOS_INCIDENTE)
    observaciones = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def validate(self, attrs):
        estado_nuevo = attrs.get('estado_incidente')
        if estado_nuevo is None:
            return attrs

        estado_actual = getattr(self.instance, 'estado_incidente', None)
        if estado_actual is None:
            if estado_nuevo != 'en_espera':
                raise serializers.ValidationError({
                    'estado_incidente': 'El incidente debe comenzar en "En espera".'
                })
            return attrs

        transiciones_permitidas = TRANSICIONES_VALIDAS.get(estado_actual, set())
        if estado_nuevo not in transiciones_permitidas:
            raise serializers.ValidationError({
                'estado_incidente': (
                    f'No se puede pasar de "{estado_actual}" a "{estado_nuevo}". '
                    f'Los estados válidos son: {sorted(transiciones_permitidas)}.'
                )
            })

        if estado_nuevo == 'observaciones_registradas':
            nueva_observacion = attrs.get('observaciones')
            observacion_actual = getattr(self.instance, 'observaciones', '') or ''
            texto = nueva_observacion if nueva_observacion is not None else observacion_actual
            if not str(texto).strip():
                raise serializers.ValidationError({
                    'observaciones': 'Las observaciones son obligatorias para registrar la etapa de observaciones.'
                })

        return attrs


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
