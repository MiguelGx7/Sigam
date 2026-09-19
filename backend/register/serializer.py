from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Usuario

# El registro publico usa las opciones viejas de este modelo (Personal/Operador/Administrador),
# pero los roles reales del sistema (usuarios.Rol) son los 5 definidos en el documento del equipo
# (D:\help\docs\ambulacias.docx). Este mapeo evita crear un rol "Personal" suelto que no exista ahi.
MAPEO_ROL_LOGIN = {
    'Personal': 'Conductor de Ambulancia',
    'Operador': 'Operador de Emergencias',
    'Administrador': 'Administrador de Institucion',
}


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

        # Este registro tambien crea la cuenta real de login (usuarios.Usuario, ver create()
        # mas abajo) -- si ese correo ya existe alli, avisar aqui en vez de fallar despues.
        from usuarios.models import Usuario as UsuarioLogin
        if UsuarioLogin.objects.filter(email=data['correo']).exists():
            raise serializers.ValidationError({"correo": "Ya existe una cuenta con este correo."})

        return data

    def create(self, validated_data):
        password_plano = validated_data['password']
        validated_data = dict(validated_data)
        validated_data.pop('confirmar_password')
        validated_data['password'] = make_password(password_plano)
        registro = super().create(validated_data)

        # El formulario de registro publico solo crea esta fila (register.Usuario). Para que
        # la persona pueda loguearse de verdad y su rol se refleje en el panel de administracion,
        # se crea tambien la cuenta correspondiente en usuarios.Usuario, con el rol asignado
        # por FK (se busca o se crea el Rol con el mismo nombre elegido en el formulario).
        from usuarios.models import Rol, Usuario as UsuarioLogin
        nombre_rol = MAPEO_ROL_LOGIN.get(registro.rol, registro.rol)
        rol_login, _ = Rol.objects.get_or_create(nombre=nombre_rol)
        UsuarioLogin.objects.create_user(
            email=registro.correo,
            nombre=f'{registro.nombre} {registro.apellido}',
            password=password_plano,
            rol=rol_login,
        )

        return registro