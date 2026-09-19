import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

const API_BASE_URL = 'http://127.0.0.1:8000';
const ACCESS_TOKEN_KEY = 'sigam_access_token';
const REFRESH_TOKEN_KEY = 'sigam_refresh_token';

export interface LoginResponse {
  access: string;
  refresh: string;
  usuario: {
    id: number;
    nombre: string;
    email: string;
    rol: number | null;
    rol_nombre: string | null;
    is_active: boolean;
  };
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = `${API_BASE_URL}/api/register/registro/`;
  private loginUrl = `${API_BASE_URL}/login/`;
  private recuperarUrl = `${API_BASE_URL}/password/recuperar/`;
  private confirmarUrl = `${API_BASE_URL}/password/confirmar/`;

  constructor(private http: HttpClient) {}

  registrarUsuario(datosFormulario: any): Observable<any> {
    // El formulario usa nombres en ingles/camelCase; el serializer de Django (register/serializer.py)
    // espera estos nombres exactos.
    const payload = {
      nombre: datosFormulario.nombre,
      apellido: datosFormulario.apellido,
      documento: datosFormulario.documento,
      telefono: datosFormulario.telefono,
      correo: datosFormulario.email,
      rol: 'Personal', // El registro publico no elige rol -- un administrador lo asigna despues desde el panel.
      password: datosFormulario.password,
      confirmar_password: datosFormulario.confirmPassword,
      acepta_terminos: datosFormulario.aceptaTerminos,
    };
    return this.http.post(this.apiUrl, payload);
  }

  login(email: string, password: string): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(this.loginUrl, { email, password }).pipe(
      tap((respuesta) => {
        localStorage.setItem(ACCESS_TOKEN_KEY, respuesta.access);
        localStorage.setItem(REFRESH_TOKEN_KEY, respuesta.refresh);
      })
    );
  }

  logout(): void {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
  }

  getAccessToken(): string | null {
    return localStorage.getItem(ACCESS_TOKEN_KEY);
  }

  isAuthenticated(): boolean {
    return !!this.getAccessToken();
  }

  recuperarPassword(email: string): Observable<any> {
    return this.http.post(this.recuperarUrl, { email });
  }

  confirmarPassword(uid: string, token: string, nuevaPassword: string): Observable<any> {
    return this.http.post(this.confirmarUrl, { uid, token, nueva_password: nuevaPassword });
  }
}
