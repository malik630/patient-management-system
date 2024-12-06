import { Injectable } from "@angular/core";
import { UseCase } from "../base/use-case";
import { PatientRepository } from "../repositories/patient.repository";


@Injectable({
    providedIn: 'root',
})
export class PatientLoginUseCase implements UseCase<{},boolean>{

    constructor(private patientRepository: PatientRepository) { }

    execute(params: {}): Promise<boolean> {
        return this.patientRepository.login(params);
    }
    
}