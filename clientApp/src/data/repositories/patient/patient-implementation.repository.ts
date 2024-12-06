import { Injectable } from "@angular/core";
import { PatientRepository } from "../../../domain/repositories/patient.repository";
import { PatientImplementationRepositoryMapper } from "./mappers/patient-repository.mapper";
import { HttpClient } from "@angular/common/http";
import { firstValueFrom } from "rxjs";

@Injectable({
    providedIn: 'root',
})
export class PatientImplementationRepository extends PatientRepository {

    patientMapper = new PatientImplementationRepositoryMapper();


    constructor(private http: HttpClient) {
        super();
    }

    

    override login(params: {}): Promise<boolean> {
        return Promise.resolve(true)
        //firstValueFrom(
          //  this.http.post<boolean>('api', {params})    
        //);
    }

    
    
}