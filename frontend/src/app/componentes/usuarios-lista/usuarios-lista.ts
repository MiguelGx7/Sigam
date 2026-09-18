import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-usuarios-lista',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './usuarios-lista.html',
  styleUrl: './usuarios-lista.css'
})
export class UsuariosLista implements OnInit {
  usuarios: any[] = [];
  isLoading = false;
  errorMessage = '';

  constructor(private authService: AuthService) {}

  getDisplayValue(value: unknown, fallback: string): string {
    if (value === null || value === undefined || value === '') {
      return fallback;
    }

    if (typeof value === 'string') {
      const text = value.trim();
      return text || fallback;
    }

    if (typeof value === 'number') {
      return String(value);
    }

    if (typeof value === 'object') {
      const objectValue = value as Record<string, unknown>;
      const objectName = typeof objectValue.nombre === 'string' ? objectValue.nombre.trim() : '';
      return objectName || fallback;
    }

    return fallback;
  }

  getRolLabel(rol: unknown): string {
    if (rol === null || rol === undefined || rol === '') {
      return 'Sin rol';
    }

    if (typeof rol === 'object') {
      const objectValue = rol as Record<string, unknown>;
      return this.getDisplayValue(objectValue.nombre, 'Sin rol');
    }

    return this.getDisplayValue(rol, 'Sin rol');
  }

  normalizarUsuarios(response: any[]): any[] {
    return response.map((usuario) => ({
      ...usuario,
      nombre: this.getDisplayValue(usuario?.nombre, 'Sin nombre'),
      username: this.getDisplayValue(usuario?.username ?? usuario?.email, 'Sin usuario'),
      email: this.getDisplayValue(usuario?.email, 'Sin correo'),
      rol: this.getRolLabel(usuario?.rol)
    }));
  }

  ngOnInit(): void {
    this.cargarUsuarios();
  }

  cargarUsuarios(): void {
    this.isLoading = true;
    this.errorMessage = '';

    this.authService.getUsuarios().subscribe({
      next: (response) => {
        this.usuarios = Array.isArray(response) ? this.normalizarUsuarios(response) : [];
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'No se pudo cargar la lista de usuarios.';
        this.isLoading = false;
      }
    });
  }
}
