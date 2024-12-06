import { Component, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { PatientLoginUseCase } from '../../domain/usecases/patient-login.usecase';
import { PatientRepository } from '../../domain/repositories/patient.repository';
import { PatientImplementationRepository } from '../../data/repositories/patient/patient-implementation.repository';
import { AuthComponent } from './auth/auth.component';


@Component({
  selector: 'app-root',
  imports: [RouterOutlet,AuthComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent {}
