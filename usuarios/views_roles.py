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


def roles_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        if not nombre:
            return render(request, 'usuarios/roles_form.html', {
                'error': 'Ingresa un nombre para el rol.',
                'nombre': nombre,
                'titulo': 'Nuevo rol',
            })

        if Rol.objects.filter(nombre__iexact=nombre).exists():
            return render(request, 'usuarios/roles_form.html', {
                'error': 'Ya existe un rol con ese nombre.',
                'nombre': nombre,
                'titulo': 'Nuevo rol',
            })

        Rol.objects.create(nombre=nombre)
        messages.success(request, 'Rol creado correctamente.')
        return redirect('roles_list')

    return render(request, 'usuarios/roles_form.html', {'titulo': 'Nuevo rol'})


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


def _api_response(datos, status=200):
    respuesta = JsonResponse(datos, safe=isinstance(datos, dict), status=status)
    respuesta['Access-Control-Allow-Origin'] = 'http://localhost:4200'
    respuesta['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    respuesta['Access-Control-Allow-Headers'] = 'Content-Type'
    return respuesta


@csrf_exempt
@require_http_methods(['GET', 'POST', 'OPTIONS'])
def roles_api(request):
    if request.method == 'OPTIONS':
        return _api_response({})
    if request.method == 'GET':
        roles = list(Rol.objects.order_by('nombre').values('id_rol', 'nombre'))
        return _api_response(roles)

    nombre = _nombre_desde_request(request)
    if not nombre:
        return _api_response({'error': 'El nombre del rol es obligatorio.'}, status=400)
    if Rol.objects.filter(nombre__iexact=nombre).exists():
        return _api_response({'error': 'Ya existe un rol con ese nombre.'}, status=400)

    rol = Rol.objects.create(nombre=nombre)
    return _api_response({'id_rol': rol.id_rol, 'nombre': rol.nombre}, status=201)


@csrf_exempt
@require_http_methods(['PUT', 'DELETE', 'OPTIONS'])
def rol_api_detail(request, id_rol):
    if request.method == 'OPTIONS':
        return _api_response({})
    rol = get_object_or_404(Rol, id_rol=id_rol)

    if request.method == 'DELETE':
        rol.delete()
        return _api_response({}, status=204)

    nombre = _nombre_desde_request(request)
    if not nombre:
        return _api_response({'error': 'El nombre del rol es obligatorio.'}, status=400)
    if Rol.objects.filter(nombre__iexact=nombre).exclude(id_rol=rol.id_rol).exists():
        return _api_response({'error': 'Ya existe un rol con ese nombre.'}, status=400)

    rol.nombre = nombre
    rol.save(update_fields=['nombre'])
    return _api_response({'id_rol': rol.id_rol, 'nombre': rol.nombre})
