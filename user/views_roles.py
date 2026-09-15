from django.http import JsonResponse
from .models import Rol


def roles_edit(request, id_rol):
    rol = Rol.objects.get(id_rol=id_rol)

    if request.method == 'POST':
        rol.nombre = request.POST.get('nombre')
        rol.save()
        return JsonResponse({'mensaje': 'Rol actualizado'})

    return JsonResponse({'id_rol': rol.id_rol, 'nombre': rol.nombre})


def roles_delete(request, id_rol):
    rol = Rol.objects.get(id_rol=id_rol)

    if request.method == 'POST':
        rol.delete()
        return JsonResponse({'mensaje': 'Rol eliminado'})

    return JsonResponse({'mensaje': 'Confirmar eliminacion', 'id_rol': rol.id_rol, 'nombre': rol.nombre})