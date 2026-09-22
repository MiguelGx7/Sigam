import { Routes } from '@angular/router';
import { Login } from './componentes/login/login';
import { Registro } from './componentes/registro/registro';
import { RecuperarPassword } from './componentes/recuperar-password/recuperar-password';
import { Layout } from './componentes/layout/layout';
import { Usuarios } from './componentes/usuarios/usuarios';
import { Roles } from './componentes/roles/roles';
import { Incidentes } from './componentes/incidentes/incidentes';
import { authGuard } from './guards/auth-guard';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: Login },
  { path: 'registro', component: Registro },
  { path: 'recuperar', component: RecuperarPassword },
  { path: 'recuperar/confirmar', component: RecuperarPassword },
  {
    path: 'panel',
    component: Layout,
    canActivate: [authGuard],
    children: [
      { path: '', redirectTo: 'incidentes', pathMatch: 'full' },
      { path: 'usuarios', component: Usuarios },
      { path: 'roles', component: Roles },
      { path: 'incidentes', component: Incidentes },
    ],
  },
  { path: '**', redirectTo: 'login' },
];
