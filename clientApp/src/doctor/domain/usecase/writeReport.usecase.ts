import { Injectable } from "@angular/core";
import { UseCase } from "../../../base/domain/usecase/use-case";
import { DoctorRepository } from "../repositories/doctor.repository";

@Injectable({
    providedIn: 'root',
})
export class WritePrescriptionUseCase implements UseCase<{},{}>{

    constructor(private doctorRepository: DoctorRepository) { }

    execute(params: {}): Promise<{}> {
        return this.doctorRepository.writeReport(params);
    }
    
}