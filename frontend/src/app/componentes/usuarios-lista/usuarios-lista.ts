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

  ngOnInit(): void {
    this.cargarUsuarios();
  }

  cargarUsuarios(): void {
    this.isLoading = true;
    this.errorMessage = '';

    this.authService.getUsuarios().subscribe({
      next: (response) => {
        this.usuarios = Array.isArray(response) ? response : [];
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'No se pudo cargar la lista de usuarios.';
        this.isLoading = false;
      }
    });
  }
}
