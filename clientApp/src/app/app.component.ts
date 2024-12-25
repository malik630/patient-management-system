import { Component } from '@angular/core';
<<<<<<< HEAD
import { RouterOutlet } from '@angular/router';
import { AuthComponent } from '../auth/presentation/auth.component';
import { DashboardComponent } from '../dashboard/presentation/dashboard.component';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, DashboardComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
=======
import { Router, RouterModule, RouterOutlet } from '@angular/router';
import { AuthRepository } from '../auth/domain/repositories/auth.repository';

@Component({
  selector: 'app-root',
  template:`<router-outlet></router-outlet>`,
  imports:[RouterModule]
>>>>>>> 25895233bdc7cb6ab79d6a74182bf7b54cd12b80
})
export class AppComponent {
   constructor(private router: Router, private authRepository: AuthRepository) {}

  ngOnInit(): void {
    if (this.authRepository.isAuthenticated()) {
      this.router.navigate(['/dashboard']);
    } else {
      this.router.navigate(['/login']);
    }
  }
}
