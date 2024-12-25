import { Component } from '@angular/core';
import { Router, RouterModule, RouterOutlet } from '@angular/router';
import { AuthRepository } from '../auth/domain/repositories/auth.repository';

@Component({
  selector: 'app-root',
  template:`<router-outlet></router-outlet>`,
  imports:[RouterModule]
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
