import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { AuthComponent } from '../auth/presentation/auth.component';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet,AuthComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent {}
