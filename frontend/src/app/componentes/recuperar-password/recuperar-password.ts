import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators, AbstractControl, ValidationErrors } from '@angular/forms';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-recuperar-password',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './recuperar-password.html',
  styleUrl: './recuperar-password.css'
})
export class RecuperarPassword implements OnInit {
  // Fase 1: pedir el correo. Fase 2 (uid/token en la URL): definir la nueva contraseña.
  modoConfirmar = false;
  uid = '';
  token = '';

  solicitarForm: FormGroup;
  confirmarForm: FormGroup;

  isLoading = false;
  errorMessage: string | null = null;
  successMessage: string | null = null;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private route: ActivatedRoute
  ) {
    this.solicitarForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
    });

    this.confirmarForm = this.fb.group({
      nuevaPassword: ['', [Validators.required, Validators.minLength(6)]],
      confirmarPassword: ['', [Validators.required]],
    }, { validators: this.passwordMatchValidator });
  }

  ngOnInit(): void {
    this.route.queryParamMap.subscribe((params) => {
      const uid = params.get('uid');
      const token = params.get('token');
      if (uid && token) {
        this.modoConfirmar = true;
        this.uid = uid;
        this.token = token;
      }
    });
  }

  private passwordMatchValidator(control: AbstractControl): ValidationErrors | null {
    const nueva = control.get('nuevaPassword')?.value;
    const confirmar = control.get('confirmarPassword')?.value;
    if (nueva && confirmar && nueva !== confirmar) {
      control.get('confirmarPassword')?.setErrors({ passwordMismatch: true });
      return { passwordMismatch: true };
    }
    return null;
  }

  isInvalidSolicitar(campo: string): boolean {
    const field = this.solicitarForm.get(campo);
    return !!(field && field.invalid && (field.dirty || field.touched));
  }

  isInvalidConfirmar(campo: string): boolean {
    const field = this.confirmarForm.get(campo);
    return !!(field && field.invalid && (field.dirty || field.touched));
  }

  onSolicitar(): void {
    if (this.solicitarForm.invalid) {
      this.solicitarForm.markAllAsTouched();
      return;
    }
    this.isLoading = true;
    this.errorMessage = null;

    this.authService.recuperarPassword(this.solicitarForm.value.email).subscribe({
      next: (respuesta) => {
        this.isLoading = false;
        this.successMessage = respuesta.mensaje;
        this.solicitarForm.reset();
      },
      error: (err: HttpErrorResponse) => {
        this.isLoading = false;
        this.errorMessage = this.extraerMensajeError(err);
      }
    });
  }

  onConfirmar(): void {
    if (this.confirmarForm.invalid) {
      this.confirmarForm.markAllAsTouched();
      return;
    }
    this.isLoading = true;
    this.errorMessage = null;

    this.authService.confirmarPassword(this.uid, this.token, this.confirmarForm.value.nuevaPassword).subscribe({
      next: (respuesta) => {
        this.isLoading = false;
        this.successMessage = respuesta.mensaje;
        this.confirmarForm.reset();
      },
      error: (err: HttpErrorResponse) => {
        this.isLoading = false;
        this.errorMessage = this.extraerMensajeError(err);
      }
    });
  }

  private extraerMensajeError(err: HttpErrorResponse): string {
    if (err.status === 0) {
      return 'No se pudo conectar con el servidor. Verifica que el backend este corriendo.';
    }
    if (err.error?.error) {
      return err.error.error;
    }
    return 'Ocurrio un error. Intenta de nuevo.';
  }
}
