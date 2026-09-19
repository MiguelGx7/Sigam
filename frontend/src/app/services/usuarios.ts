import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

const API_BASE_URL = 'http://127.0.0.1:8000';

export interface Usuario {
  id: number;
  nombre: string;
  email: string;
  rol: number | null;
  rol_nombre: string | null;
  is_active: boolean;
}

export interface Rol {
  id_rol: number;
  nombre: string;
}

@Injectable({
  providedIn: 'root'
})
export class UsuariosService {
  private usuariosUrl = `${API_BASE_URL}/usuarios/`;
  private rolesUrl = `${API_BASE_URL}/roles/`;

  constructor(private http: HttpClient) {}

  listar(): Observable<Usuario[]> {
    return this.http.get<Usuario[]>(this.usuariosUrl);
  }

  listarRoles(): Observable<Rol[]> {
    return this.http.get<Rol[]>(this.rolesUrl);
  }

  crearRol(nombre: string): Observable<Rol> {
    return this.http.post<Rol>(this.rolesUrl, { nombre });
  }

  actualizarNombreRol(idRol: number, nombre: string): Observable<Rol> {
    return this.http.put<Rol>(`${this.rolesUrl}${idRol}/`, { nombre });
  }

  eliminarRol(idRol: number): Observable<void> {
    return this.http.delete<void>(`${this.rolesUrl}${idRol}/`);
  }

  crearUsuario(datos: { nombre: string; email: string; rol: number | null; password: string; is_active: boolean }): Observable<Usuario> {
    return this.http.post<Usuario>(`${API_BASE_URL}/usuarios/crear/`, {
      nombre: datos.nombre,
      email: datos.email,
      rol: datos.rol,
      password: datos.password,
      is_active: datos.is_active,
    });
  }

  actualizarUsuario(id: number, datos: { nombre: string; email: string; rol: number | null; password?: string; is_active: boolean }): Observable<Usuario> {
    const payload: { nombre: string; email: string; rol: number | null; is_active: boolean; password?: string } = {
      nombre: datos.nombre,
      email: datos.email,
      rol: datos.rol,
      is_active: datos.is_active,
    };

    if (datos.password) {
      payload.password = datos.password;
    }

    return this.http.put<Usuario>(`${API_BASE_URL}/usuarios/editar/${id}/`, payload);
  }

  actualizarRol(usuario: Usuario, idRol: number | null): Observable<Usuario> {
    // El backend (CrearUsuario.put en usuarios/views_usuario.py) espera el objeto completo,
    // no un PATCH parcial.
    const payload = {
      nombre: usuario.nombre,
      email: usuario.email,
      rol: idRol,
      is_active: usuario.is_active,
    };
    return this.actualizarUsuario(usuario.id, payload);
  }

  eliminar(id: number): Observable<any> {
    return this.http.delete(`${API_BASE_URL}/usuarios/eliminar/${id}/`);
  }
}
