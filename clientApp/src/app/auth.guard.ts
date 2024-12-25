import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthRepository } from '../auth/domain/repositories/auth.repository';

export const authGuard: CanActivateFn = (route, state) => {
  const authRepository = inject(AuthRepository);  
  const router = inject(Router); 
  if (authRepository.isAuthenticated()) {
    return true;  
  } else {
    router.navigate(['/login']);  
    return false;  
  }
};
