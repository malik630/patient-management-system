import { Injectable } from "@angular/core";
import { DoctorRepository } from "../repositories/doctor.repository";
import { UseCase } from "../../../base/domain/usecase/use-case";

@Injectable({
    providedIn: 'root',
})
export class GetDPIUseCase implements UseCase<{},{}>{

    constructor(private doctorRepository: DoctorRepository) { }

    execute(params: {}): Promise<{}> {
        return this.doctorRepository.getDPI(params);
    }
    
}