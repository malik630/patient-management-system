import { Routes } from '@angular/router';
import { AuthComponent } from '../auth/presentation/auth.component';
import { DashboardComponent } from '../dashboard/presentation/dashboard.componant';
import { authGuard } from './auth.guard';

export const routes: Routes = [
    { path: 'login', component: AuthComponent },
  { path: 'dashboard',canActivate: [authGuard], component: DashboardComponent },
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: '**', redirectTo: '/login' }
];
