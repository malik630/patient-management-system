import { Injectable } from "@angular/core";

@Injectable({
    providedIn: 'root',
})
export abstract class DoctorRepository {
    abstract getDPI(params: {}): Promise<{}>;
    abstract searchDPI(params : {}): Promise<{}>;
    abstract writePrescription(params : {}): Promise<{}>;
    abstract writePrescription(params : {}): Promise<{}>;
    abstract writeSummary(params : {}): Promise<{}>;
    abstract writeReport(params : {}): Promise<{}>;

}