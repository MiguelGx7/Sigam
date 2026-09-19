import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { Rol, UsuariosService } from '../../services/usuarios';

@Component({
  selector: 'app-roles',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './roles.html',
  styleUrl: './roles.css'
})
export class Roles implements OnInit {
  private readonly ordenOficial = [
    'Super Administrador',
    'Administrador de Institucion',
    'Operador de Emergencias',
    'Conductor de Ambulancia',
    'Auditor',
  ];

  roles: Rol[] = [];
  cargando = true;
  modalAbierto = false;
  rolEditando: Rol | null = null;
  rolForm: FormGroup;
  errorMessage: string | null = null;
  successMessage: string | null = null;

  constructor(
    private usuariosService: UsuariosService,
    private fb: FormBuilder
  ) {
    this.rolForm = this.fb.group({
      nombre: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(100)]],
    });
  }

  ngOnInit(): void {
    this.cargarRoles();
  }

  cargarRoles(): void {
    this.cargando = true;
    this.usuariosService.listarRoles().subscribe({
      next: (roles) => {
        this.roles = this.ordenarRoles(roles);
        this.cargando = false;
      },
      error: (err) => {
        this.errorMessage = this.extraerMensajeError(err);
        this.cargando = false;
      },
    });
  }

  abrirModal(rol?: Rol): void {
    this.rolEditando = rol ?? null;
    this.rolForm.reset({ nombre: rol?.nombre ?? '' });
    this.modalAbierto = true;
  }

  cerrarModal(): void {
    this.modalAbierto = false;
    this.rolEditando = null;
    this.rolForm.reset();
  }

  guardarRol(): void {
    if (this.rolForm.invalid) {
      this.rolForm.markAllAsTouched();
      return;
    }

    this.limpiarMensajes();
    const nombre = this.rolForm.value.nombre.trim();
    const solicitud = this.rolEditando
      ? this.usuariosService.actualizarNombreRol(this.rolEditando.id_rol, nombre)
      : this.usuariosService.crearRol(nombre);

    solicitud.subscribe({
      next: () => {
        this.successMessage = this.rolEditando ? 'Rol actualizado correctamente.' : 'Rol creado correctamente.';
        this.cerrarModal();
        this.cargarRoles();
      },
      error: (err) => (this.errorMessage = this.extraerMensajeError(err)),
    });
  }

  eliminarRol(rol: Rol): void {
    if (!confirm(`¿Eliminar el rol ${rol.nombre}?`)) {
      return;
    }

    this.limpiarMensajes();
    this.usuariosService.eliminarRol(rol.id_rol).subscribe({
      next: () => {
        this.roles = this.roles.filter((item) => item.id_rol !== rol.id_rol);
        this.successMessage = 'Rol eliminado correctamente.';
      },
      error: (err) => (this.errorMessage = this.extraerMensajeError(err)),
    });
  }

  get esEdicion(): boolean {
    return this.rolEditando !== null;
  }

  private limpiarMensajes(): void {
    this.errorMessage = null;
    this.successMessage = null;
  }

  private ordenarRoles(roles: Rol[]): Rol[] {
    return [...roles].sort((rolA, rolB) => {
      const prioridadA = this.obtenerPrioridad(rolA.nombre);
      const prioridadB = this.obtenerPrioridad(rolB.nombre);

      if (prioridadA !== prioridadB) {
        return prioridadA - prioridadB;
      }

      return rolA.nombre.localeCompare(rolB.nombre, 'es');
    });
  }

  private obtenerPrioridad(nombre: string): number {
    const nombreNormalizado = nombre.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    const posicion = this.ordenOficial.indexOf(nombreNormalizado);
    return posicion === -1 ? this.ordenOficial.length : posicion;
  }

  private extraerMensajeError(err: HttpErrorResponse): string {
    if (err.status === 0) {
      return 'No se pudo conectar con el servidor. Verifica que el backend este corriendo.';
    }
    if (err.status === 401) {
      return 'Tu sesión expiró. Vuelve a iniciar sesión.';
    }
    if (err.error && typeof err.error === 'object') {
      return Object.values(err.error).flat().join(' ');
    }
    return 'Ocurrió un error. Intenta de nuevo.';
  }
}
