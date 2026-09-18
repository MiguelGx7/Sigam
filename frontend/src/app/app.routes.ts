import { Routes } from '@angular/router';
import { Registro } from './componentes/registro/registro';
import { UsuariosLista } from './componentes/usuarios-lista/usuarios-lista';

export const routes: Routes = [
  { path: '', redirectTo: 'registro', pathMatch: 'full' },
  { path: 'registro', component: Registro },
  { path: 'usuarios', component: UsuariosLista }
];
