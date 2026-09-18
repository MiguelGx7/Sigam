import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormControl, ReactiveFormsModule, Validators } from '@angular/forms';

interface Rol { id_rol: number; nombre: string; }

@Component({ selector: 'app-roles', standalone: true, imports: [CommonModule, ReactiveFormsModule], templateUrl: './roles.html', styleUrl: './roles.css' })
export class RolesComponent implements OnInit {
  private readonly api = 'http://127.0.0.1:8000/api/roles/';
  roles: Rol[] = []; editando: Rol | null = null; mensaje = ''; error = ''; cargando = false;
  nombre = new FormControl('', { nonNullable: true, validators: [Validators.required, Validators.maxLength(100)] });
  constructor(private http: HttpClient) {}
  ngOnInit(): void { this.cargarRoles(); }
  cargarRoles(): void { this.cargando = true; this.http.get<Rol[]>(this.api).subscribe({ next: roles => { this.roles = roles; this.cargando = false; }, error: () => { this.error = 'No fue posible cargar los roles.'; this.cargando = false; } }); }
  guardar(): void { if (this.nombre.invalid) { this.nombre.markAsTouched(); return; } this.error = ''; const datos = { nombre: this.nombre.value.trim() }; const solicitud = this.editando ? this.http.put<Rol>(`${this.api}${this.editando.id_rol}/`, datos) : this.http.post<Rol>(this.api, datos); solicitud.subscribe({ next: () => { this.mensaje = this.editando ? 'Rol actualizado correctamente.' : 'Rol creado correctamente.'; this.cancelar(); this.cargarRoles(); }, error: r => this.error = r.error?.error || 'No se pudo guardar el rol.' }); }
  editar(rol: Rol): void { this.editando = rol; this.nombre.setValue(rol.nombre); this.error = ''; this.mensaje = ''; }
  cancelar(): void { this.editando = null; this.nombre.reset(); }
  eliminar(rol: Rol): void { if (!confirm(`¿Eliminar el rol “${rol.nombre}”?`)) return; this.http.delete(`${this.api}${rol.id_rol}/`).subscribe({ next: () => { this.mensaje = 'Rol eliminado correctamente.'; this.cargarRoles(); }, error: () => this.error = 'No se pudo eliminar el rol.' }); }
}
