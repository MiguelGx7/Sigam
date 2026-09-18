import { Routes } from '@angular/router';
import { Registro } from './componentes/registro/registro';
import { RolesComponent } from './componentes/roles/roles';

export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'roles' },
  { path: 'roles', component: RolesComponent },
  { path: 'registro', component: Registro },
];
