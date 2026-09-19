from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import Rol, SolicitudCambioPassword, Usuario


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id_rol', 'nombre']


class UsuarioSerializer(serializers.ModelSerializer):
    rol_nombre = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True, required=False, min_length=6)

    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'email', 'rol', 'rol_nombre', 'is_active', 'password']

    def validate(self, data):
        if self.instance is None and not data.get('password'):
            raise serializers.ValidationError({'password': 'La contraseña es obligatoria.'})
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        return Usuario.objects.create_user(password=password, **validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for atributo, valor in validated_data.items():
            setattr(instance, atributo, valor)

        if password:
            instance.set_password(password)

        instance.save()
        return instance

    def get_rol_nombre(self, obj):
        return obj.rol.nombre if obj.rol else None


class SolicitudCambioPasswordSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.nombre', read_only=True)
    usuario_email = serializers.EmailField(source='usuario.email', read_only=True)

    class Meta:
        model = SolicitudCambioPassword
        fields = ['id', 'usuario', 'usuario_nombre', 'usuario_email', 'creada_en']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        usuario = authenticate(username=email, password=password)

        if not usuario:
            raise serializers.ValidationError('Email o contraseña incorrectos')

        if not usuario.is_active:
            raise serializers.ValidationError('Usuario inactivo')

        data['usuario'] = usuario
        return data
