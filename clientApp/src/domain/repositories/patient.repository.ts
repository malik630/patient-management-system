import { Injectable } from '@angular/core';
import { PatientModel } from '../models/patient.model';

@Injectable({
    providedIn: 'root',
})
export abstract class PatientRepository {
    abstract login(params: {}): Promise<boolean>;
}