from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'email', 'rol', 'is_active']
        # password queda afuera a propósito


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