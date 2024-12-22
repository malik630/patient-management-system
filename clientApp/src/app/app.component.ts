import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { AuthComponent } from '../auth/presentation/auth.component';
import { DashboardComponent } from '../dashboard/presentation/dashboard.componant';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet,AuthComponent,DashboardComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent {}
