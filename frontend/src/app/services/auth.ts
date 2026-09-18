import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface UsuarioPayload {
  username: string;
  nombre: string;
  email: string;
  password: string;
  rol?: number | null;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = '/api';

  constructor(private http: HttpClient) {}

  getUsuarios(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/usuarios/`);
  }

  registrarUsuario(datosUsuario: any): Observable<any> {
    const payload: UsuarioPayload = {
      username: datosUsuario.username || datosUsuario.email,
      nombre: datosUsuario.nombre?.trim() || '',
      email: datosUsuario.email,
      password: datosUsuario.password,
    };

    if (datosUsuario.rol && !Number.isNaN(Number(datosUsuario.rol))) {
      payload.rol = Number(datosUsuario.rol);
    }

    return this.http.post(`${this.apiUrl}/usuarios/crear/`, payload);
  }
}