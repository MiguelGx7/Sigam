import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { UsuariosService, Usuario, Rol, SolicitudCambioPassword } from '../../services/usuarios';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-usuarios',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, FormsModule],
  templateUrl: './usuarios.html',
  styleUrl: './usuarios.css'
})
export class Usuarios implements OnInit {
  usuarios: Usuario[] = [];
  roles: Rol[] = [];
  solicitudesPassword: SolicitudCambioPassword[] = [];
  cargando = true;

  modalAbierto = false;
  nuevoUsuarioForm: FormGroup;
  mostrarContrasena = false;
  usuarioEditando: Usuario | null = null;
  usuarioParaCambiarContrasena: Usuario | null = null;
  modalCambiarContrasenaAbierto = false;
  cambiarContrasenaForm: FormGroup;
  esSuperAdministrador = false;

  errorMessage: string | null = null;
  successMessage: string | null = null;

  constructor(
    private usuariosService: UsuariosService,
    private authService: AuthService,
    private fb: FormBuilder
  ) {
    this.nuevoUsuarioForm = this.fb.group({
      nombre: ['', [Validators.required, Validators.minLength(2)]],
      email: ['', [Validators.required, Validators.email]],
      rol: [null],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmarPassword: ['', Validators.required],
      is_active: [true],
    }, { validators: this.validarCoincidenciaContrasenas });

    this.cambiarContrasenaForm = this.fb.group({
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmarPassword: ['', Validators.required],
    }, { validators: this.validarCoincidenciaContrasenas });
  }

  ngOnInit(): void {
    this.esSuperAdministrador = this.authService.esSuperAdministrador();
    this.cargarDatos();
  }

  cargarDatos(): void {
    this.cargando = true;
    this.usuariosService.listar().subscribe({
      next: (usuarios) => {
        this.usuarios = usuarios;
        this.cargando = false;
      },
      error: (err) => {
        this.errorMessage = this.extraerMensajeError(err);
        this.cargando = false;
      },
    });
    this.usuariosService.listarRoles().subscribe({
      next: (roles) => (this.roles = roles),
      error: (err) => (this.errorMessage = this.extraerMensajeError(err)),
    });
    // Se consulta siempre: el backend es la fuente real del permiso.
    // Esto también funciona con sesiones iniciadas antes de guardar el rol en localStorage.
    this.cargarSolicitudesPassword();
  }

  cargarSolicitudesPassword(): void {
    this.usuariosService.listarSolicitudesPassword().subscribe({
      next: (solicitudes) => {
        this.esSuperAdministrador = true;
        this.solicitudesPassword = solicitudes;
      },
      error: (err) => {
        if (err.status === 403) {
          this.esSuperAdministrador = false;
          this.solicitudesPassword = [];
          return;
        }
        this.errorMessage = this.extraerMensajeError(err);
      },
    });
  }

  abrirModal(usuario?: Usuario): void {
    const usuarioParaEditar = usuario ?? null;
    this.usuarioEditando = usuarioParaEditar;
    const password = this.nuevoUsuarioForm.get('password');
    const confirmarPassword = this.nuevoUsuarioForm.get('confirmarPassword');

    if (usuarioParaEditar) {
      password?.clearValidators();
      confirmarPassword?.clearValidators();
      this.nuevoUsuarioForm.reset({
        nombre: usuarioParaEditar.nombre,
        email: usuarioParaEditar.email,
        rol: usuarioParaEditar.rol,
        password: '',
        confirmarPassword: '',
        is_active: usuarioParaEditar.is_active,
      });
    } else {
      password?.setValidators([Validators.required, Validators.minLength(6)]);
      confirmarPassword?.setValidators([Validators.required]);
      this.nuevoUsuarioForm.reset({ rol: null, is_active: true });
    }

    password?.updateValueAndValidity();
    confirmarPassword?.updateValueAndValidity();
    this.mostrarContrasena = false;
    this.modalAbierto = true;
  }

  cerrarModal(): void {
    this.modalAbierto = false;
    this.usuarioEditando = null;
  }

  guardarUsuario(): void {
    if (this.nuevoUsuarioForm.invalid) {
      this.nuevoUsuarioForm.markAllAsTouched();
      return;
    }
    this.limpiarMensajes();
    const datos = this.nuevoUsuarioForm.value;
    const solicitud = this.usuarioEditando
      ? this.usuariosService.actualizarUsuario(this.usuarioEditando.id, datos)
      : this.usuariosService.crearUsuario(datos);

    solicitud.subscribe({
      next: () => {
        this.successMessage = this.usuarioEditando
          ? 'Usuario actualizado correctamente.'
          : 'Usuario creado correctamente.';
        this.modalAbierto = false;
        this.usuarioEditando = null;
        this.cargarDatos();
      },
      error: (err) => (this.errorMessage = this.extraerMensajeError(err)),
    });
  }

  get esEdicion(): boolean {
    return this.usuarioEditando !== null;
  }

  alternarVisibilidadContrasena(): void {
    this.mostrarContrasena = !this.mostrarContrasena;
  }

  onCambiarRol(usuario: Usuario, event: Event): void {
    const valor = (event.target as HTMLSelectElement).value;
    const idRol = valor ? Number(valor) : null;
    this.limpiarMensajes();

    this.usuariosService.actualizarRol(usuario, idRol).subscribe({
      next: (actualizado) => {
        usuario.rol = actualizado.rol;
        usuario.rol_nombre = actualizado.rol_nombre;
        this.successMessage = `Rol de ${usuario.nombre} actualizado.`;
      },
      error: (err) => (this.errorMessage = this.extraerMensajeError(err)),
    });
  }

  eliminarUsuario(usuario: Usuario): void {
    if (!confirm(`¿Eliminar al usuario ${usuario.nombre}?`)) {
      return;
    }
    this.limpiarMensajes();
    this.usuariosService.eliminar(usuario.id).subscribe({
      next: () => {
        this.usuarios = this.usuarios.filter((u) => u.id !== usuario.id);
        this.successMessage = 'Usuario eliminado.';
      },
      error: (err) => (this.errorMessage = this.extraerMensajeError(err)),
    });
  }

  abrirCambioContrasena(usuario: Usuario): void {
    this.usuarioParaCambiarContrasena = usuario;
    this.cambiarContrasenaForm.reset();
    this.modalCambiarContrasenaAbierto = true;
  }

  cerrarCambioContrasena(): void {
    this.modalCambiarContrasenaAbierto = false;
    this.usuarioParaCambiarContrasena = null;
    this.cambiarContrasenaForm.reset();
  }

  cambiarContrasenaComoAdministrador(): void {
    if (!this.usuarioParaCambiarContrasena || this.cambiarContrasenaForm.invalid) {
      this.cambiarContrasenaForm.markAllAsTouched();
      return;
    }

    this.limpiarMensajes();
    const password = this.cambiarContrasenaForm.value.password;
    this.usuariosService.cambiarPasswordAdministrativa(this.usuarioParaCambiarContrasena.id, password).subscribe({
      next: (respuesta) => {
        this.successMessage = `Contraseña de ${this.usuarioParaCambiarContrasena?.nombre} actualizada. ${respuesta.mensaje}`;
        this.cerrarCambioContrasena();
        this.cargarSolicitudesPassword();
      },
      error: (err) => (this.errorMessage = this.extraerMensajeError(err)),
    });
  }

  private limpiarMensajes(): void {
    this.errorMessage = null;
    this.successMessage = null;
  }

  private validarCoincidenciaContrasenas(formulario: FormGroup) {
    const password = formulario.get('password')?.value;
    const confirmarPassword = formulario.get('confirmarPassword')?.value;

    if (password && !confirmarPassword) {
      formulario.get('confirmarPassword')?.setErrors({ required: true });
      return { passwordConfirmationRequired: true };
    }

    if (password && confirmarPassword && password !== confirmarPassword) {
      formulario.get('confirmarPassword')?.setErrors({ passwordMismatch: true });
      return { passwordMismatch: true };
    }
    return null;
  }

  private extraerMensajeError(err: HttpErrorResponse): string {
    if (err.status === 0) {
      return 'No se pudo conectar con el servidor. Verifica que el backend este corriendo.';
    }
    if (err.status === 401) {
      return 'Tu sesion expiro. Vuelve a iniciar sesion.';
    }
    const errores = err.error;
    if (errores && typeof errores === 'object') {
      return Object.values(errores).flat().join(' ');
    }
    return 'Ocurrio un error. Intenta de nuevo.';
  }
}
