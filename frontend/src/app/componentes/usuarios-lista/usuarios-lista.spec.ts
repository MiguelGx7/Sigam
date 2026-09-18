import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { HttpClientTestingModule } from '@angular/common/http/testing';

import { UsuariosLista } from './usuarios-lista';

describe('UsuariosLista', () => {
  let component: UsuariosLista;
  let fixture: ComponentFixture<UsuariosLista>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UsuariosLista, HttpClientTestingModule],
      providers: [provideRouter([])],
    }).compileComponents();

    fixture = TestBed.createComponent(UsuariosLista);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should normalize missing values to avoid blank cells', () => {
    const usuarios = [
      { nombre: '', username: '', email: '', rol: null },
      { nombre: 'Ana', username: 'ana', email: 'ana@test.com', rol: { nombre: 'Administrador' } }
    ];

    const result = component.normalizarUsuarios(usuarios);

    expect(result[0].nombre).toBe('Sin nombre');
    expect(result[0].username).toBe('Sin usuario');
    expect(result[0].email).toBe('Sin correo');
    expect(result[0].rol).toBe('Sin rol');
    expect(result[1].rol).toBe('Administrador');
  });
});
