from rest_framework import serializers

from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        usuario = Usuario(**validated_data)

        if password is not None:
            usuario.set_password(password)

        usuario.save()
        return usuario

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance
