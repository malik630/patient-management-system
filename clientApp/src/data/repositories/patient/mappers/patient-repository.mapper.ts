import { Mapper } from "../../../../base/utiles/mapper";
import { PatientModel } from "../../../../domain/models/patient.model";
import { PatientEntity } from "../entities/patient-entity";

export class PatientImplementationRepositoryMapper extends Mapper<PatientEntity, PatientModel> {
    mapFrom(param: PatientEntity): PatientModel {
        return {
            id: param.id,
            fullName: param.fullName,
            username: param.username,
            NSS: param.NSS,
            phoneNum: param.phoneNum,
            profilePicture: param.profilePicture

        };
    }
    mapTo(param: PatientModel): PatientEntity {
        return {
            id: param.id,
            fullName: param.fullName,
            username: param.username,
            NSS: param.NSS,
            phoneNum: param.phoneNum,
            profilePicture: param.profilePicture
        }
    }
}