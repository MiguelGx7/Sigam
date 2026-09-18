from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Rol


def roles_list(request):
    return render(request, 'usuarios/roles_list.html', {
        'roles': Rol.objects.order_by('nombre'),
    })


def roles_edit(request, id_rol):
    rol = get_object_or_404(Rol, id_rol=id_rol)

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        if not nombre:
            return render(request, 'usuarios/roles_form.html', {
                'rol': rol,
                'nombre': nombre,
                'titulo': 'Editar rol',
                'error': 'Ingresa un nombre para el rol.',
            })
        if Rol.objects.filter(nombre__iexact=nombre).exclude(id_rol=rol.id_rol).exists():
            return render(request, 'usuarios/roles_form.html', {
                'rol': rol,
                'nombre': nombre,
                'titulo': 'Editar rol',
                'error': 'Ya existe un rol con ese nombre.',
            })

        rol.nombre = nombre
        rol.save()
        messages.success(request, 'Rol actualizado correctamente.')
        return redirect('roles_list')

    return render(request, 'usuarios/roles_form.html', {
        'rol': rol,
        'titulo': 'Editar rol',
    })


def roles_delete(request, id_rol):
    rol = get_object_or_404(Rol, id_rol=id_rol)

    if request.method == 'POST':
        rol.delete()
        messages.success(request, 'Rol eliminado correctamente.')
        return redirect('roles_list')

    return render(request, 'usuarios/roles_form.html', {
        'rol': rol,
        'titulo': 'Eliminar rol',
        'eliminar': True,
    })


def _nombre_desde_request(request):
    try:
        datos = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return ''
    return datos.get('nombre', '').strip()


def _api_response(request, datos, status=200):
    respuesta = JsonResponse(datos, safe=isinstance(datos, dict), status=status)
    origen = request.headers.get('Origin')
    if origen in {'http://localhost:4200', 'http://127.0.0.1:4200'}:
        respuesta['Access-Control-Allow-Origin'] = origen
    else:
        respuesta['Access-Control-Allow-Origin'] = 'http://localhost:4200'
    respuesta['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    respuesta['Access-Control-Allow-Headers'] = 'Content-Type'
    return respuesta


@csrf_exempt
@require_http_methods(['GET', 'OPTIONS'])
def roles_api(request):
    if request.method == 'OPTIONS':
        return _api_response(request, {})
    roles = list(Rol.objects.order_by('nombre').values('id_rol', 'nombre'))
    return _api_response(request, roles)


@csrf_exempt
@require_http_methods(['PUT', 'DELETE', 'OPTIONS'])
def rol_api_detail(request, id_rol):
    if request.method == 'OPTIONS':
        return _api_response(request, {})
    rol = get_object_or_404(Rol, id_rol=id_rol)

    if request.method == 'DELETE':
        rol.delete()
        return _api_response(request, {}, status=204)

    nombre = _nombre_desde_request(request)
    if not nombre:
        return _api_response(request, {'error': 'El nombre del rol es obligatorio.'}, status=400)
    if Rol.objects.filter(nombre__iexact=nombre).exclude(id_rol=rol.id_rol).exists():
        return _api_response(request, {'error': 'Ya existe un rol con ese nombre.'}, status=400)

    rol.nombre = nombre
    rol.save(update_fields=['nombre'])
    return _api_response(request, {'id_rol': rol.id_rol, 'nombre': rol.nombre})
