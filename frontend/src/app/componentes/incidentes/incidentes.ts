import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { DespachoService, Incidente, EstadoIncidente } from '../../services/despacho';

const ESTADOS: { value: EstadoIncidente; label: string }[] = [
  { value: 'en_espera', label: 'En espera' },
  { value: 'llegada_incidente_confirmada', label: 'Llegada al incidente confirmada' },
  { value: 'observaciones_registradas', label: 'Observaciones registradas' },
  { value: 'traslado_iniciado', label: 'Traslado iniciado' },
  { value: 'hospital_seleccionado', label: 'Hospital seleccionado' },
  { value: 'llegada_hospital_confirmada', label: 'Llegada al hospital confirmada' },
  { value: 'cerrado', label: 'Cerrado' },
];

@Component({
  selector: 'app-incidentes',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './incidentes.html',
  styleUrl: './incidentes.css',
})
export class Incidentes implements OnInit {
  incidentes: Incidente[] = [];
  cargando = true;
  error = '';
  exito = '';

  constructor(private despachoService: DespachoService) {}

  ngOnInit(): void {
    this.cargarIncidentes();
  }

  cargarIncidentes(): void {
    this.cargando = true;
    this.error = '';
    this.despachoService.listarIncidentes().subscribe({
      next: (incidentes) => {
        this.incidentes = incidentes;
        this.cargando = false;
      },
      error: () => {
        this.error = 'No se pudieron cargar los incidentes.';
        this.cargando = false;
      },
    });
  }

  actualizar(incidente: Incidente): void {
    const estado = incidente.estado_incidente ?? 'en_espera';
    this.despachoService
      .actualizarEstadoIncidente(incidente.id, estado as EstadoIncidente, incidente.observaciones ?? '')
      .subscribe({
        next: () => {
          this.exito = `Incidente #${incidente.id} actualizado correctamente.`;
          this.cargarIncidentes();
        },
        error: () => {
          this.error = 'No se pudo actualizar el incidente.';
        },
      });
  }

  getEstados(): { value: EstadoIncidente; label: string }[] {
    return ESTADOS;
  }
}
