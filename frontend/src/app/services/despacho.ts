import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

const API_BASE_URL = 'http://127.0.0.1:8000';

export type EstadoIncidente =
  | 'en_espera'
  | 'llegada_incidente_confirmada'
  | 'observaciones_registradas'
  | 'traslado_iniciado'
  | 'hospital_seleccionado'
  | 'llegada_hospital_confirmada'
  | 'cerrado';

export interface Incidente {
  id: number;
  solicitud_id?: number | null;
  tipo_id?: number | null;
  prioridad_id?: number | null;
  descripcion?: string | null;
  observaciones?: string | null;
  fecha_hora?: string | null;
  ubicacion?: string | null;
  estado_incidente?: EstadoIncidente | null;
}

@Injectable({
  providedIn: 'root',
})
export class DespachoService {
  private incidentesUrl = `${API_BASE_URL}/api/despacho/incidentes/`;

  constructor(private http: HttpClient) {}

  listarIncidentes(): Observable<Incidente[]> {
    return this.http.get<Incidente[]>(this.incidentesUrl);
  }

  actualizarEstadoIncidente(
    id: number,
    estado: EstadoIncidente,
    observaciones?: string | null,
  ): Observable<Incidente> {
    return this.http.patch<Incidente>(`${this.incidentesUrl}${id}/estado/`, {
      estado_incidente: estado,
      observaciones: observaciones ?? '',
    });
  }
}
