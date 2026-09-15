import { Component } from '@angular/core';
import { Registro } from './componentes/registro/registro';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [Registro],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class AppComponent {
  title = 'frontend';
}