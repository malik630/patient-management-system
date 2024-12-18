import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideHttpClient, withFetch } from '@angular/common/http';
import { AuthRepository } from '../auth/domain/repositories/auth.repository';
import { AuthImplementationRepository } from '../auth/data/repositories/auth-implementation.repository';
import { LoginUseCase } from '../auth/domain/usecase/login.usecase';

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes), 
    provideClientHydration(withEventReplay()), 
    provideAnimationsAsync(),
    { provide: AuthRepository, useClass: AuthImplementationRepository }, // Provide repository implementation
    { provide: LoginUseCase, useClass: LoginUseCase }, // Provide use case
    provideHttpClient(withFetch()), provideAnimationsAsync(),
  
  ]
};