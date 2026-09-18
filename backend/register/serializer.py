from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    confirmar_password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id', 'nombre', 'apellido', 'documento',
            'telefono', 'correo', 'rol', 'password',
            'confirmar_password', 'acepta_terminos'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data.get('password') != data.get('confirmar_password'):
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        
        if not data.get('acepta_terminos'):
            raise serializers.ValidationError({"acepta_terminos": "Debes aceptar los términos y condiciones."})
        
        return data

    def create(self, validated_data):
        validated_data.pop('confirmar_password')
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)