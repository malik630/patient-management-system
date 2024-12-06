import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { PatientRepository } from '../../domain/repositories/patient.repository';
import { PatientImplementationRepository } from '../../data/repositories/patient/patient-implementation.repository';
import { PatientLoginUseCase } from '../../domain/usecases/patient-login.usecase';
import { provideHttpClient, withFetch } from '@angular/common/http';

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes), 
    provideClientHydration(withEventReplay()), 
    provideAnimationsAsync(),
    { provide: PatientRepository, useClass: PatientImplementationRepository }, // Provide repository implementation
    { provide: PatientLoginUseCase, useClass: PatientLoginUseCase }, // Provide use case
    provideHttpClient(withFetch()),
  
  ]
};