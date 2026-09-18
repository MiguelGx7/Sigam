import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { FormControl, ReactiveFormsModule, Validators } from '@angular/forms';

interface Rol { id_rol: number; nombre: string; }

@Component({ selector: 'app-roles', standalone: true, imports: [CommonModule, ReactiveFormsModule], templateUrl: './roles.html', styleUrl: './roles.css' })
export class RolesComponent implements OnInit {
  private readonly api = 'http://127.0.0.1:8000/api/roles/';
  roles: Rol[] = []; editando: Rol | null = null; mensaje = ''; error = ''; cargando = false;
  nombre = new FormControl('', { nonNullable: true, validators: [Validators.required, Validators.maxLength(100)] });
  constructor(private http: HttpClient, private changeDetector: ChangeDetectorRef) {}
  ngOnInit(): void { this.cargarRoles(); }
  cargarRoles(): void {
    this.cargando = true;
    fetch(this.api)
      .then(respuesta => {
        if (!respuesta.ok) throw new Error('No se pudieron cargar los roles.');
        return respuesta.json() as Promise<Rol[]>;
      })
      .then(roles => {
        this.roles = roles;
        this.cargando = false;
        this.changeDetector.detectChanges();
      })
      .catch(() => {
        this.error = 'No fue posible cargar los roles.';
        this.cargando = false;
        this.changeDetector.detectChanges();
      });
  }
  guardar(): void { if (!this.editando || this.nombre.invalid) { this.nombre.markAsTouched(); return; } this.error = ''; const datos = { nombre: this.nombre.value.trim() }; this.http.put<Rol>(`${this.api}${this.editando.id_rol}/`, datos).subscribe({ next: () => { this.mensaje = 'Rol actualizado correctamente.'; this.cancelar(); this.cargarRoles(); }, error: r => this.error = r.error?.error || 'No se pudo guardar el rol.' }); }
  editar(rol: Rol): void { this.editando = rol; this.nombre.setValue(rol.nombre); this.error = ''; this.mensaje = ''; }
  cancelar(): void { this.editando = null; this.nombre.reset(); }
  eliminar(rol: Rol): void { if (!confirm(`¿Eliminar el rol “${rol.nombre}”?`)) return; this.http.delete(`${this.api}${rol.id_rol}/`).subscribe({ next: () => { this.mensaje = 'Rol eliminado correctamente.'; this.cargarRoles(); }, error: () => this.error = 'No se pudo eliminar el rol.' }); }
}
