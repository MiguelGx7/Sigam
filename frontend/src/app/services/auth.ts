import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'https://tu-backend-api.com/api/auth/registro'; // Cambia esto a la URL de tu API

  constructor(private http: HttpClient) {}

  registrarUsuario(datosUsuario: any): Observable<any> {
    return this.http.post(this.apiUrl, datosUsuario);
  }
}