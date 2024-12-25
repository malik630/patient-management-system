import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { DoctorRepository } from "../../domain/repositories/doctor.repository";

@Injectable({
    providedIn: 'root',
})
export class DoctorImplementationRepository extends DoctorRepository {

     constructor(private http: HttpClient) {
        super();
    }
    
    override getDPI(params: {}): Promise<{}> {
        throw new Error("Method not implemented.");
    }
    override searchDPI(params: {}): Promise<{}> {
        throw new Error("Method not implemented.");
    }

    override writePrescription(params: unknown): Promise<{}> {
        throw new Error("Method not implemented.");
    }
    override writeSummary(params: {}): Promise<{}> {
        throw new Error("Method not implemented.");
    }
    override writeReport(params: {}): Promise<{}> {
        throw new Error("Method not implemented.");
    }


    

    
    
}