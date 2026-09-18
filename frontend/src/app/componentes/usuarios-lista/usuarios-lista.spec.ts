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
});
