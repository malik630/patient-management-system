import { Injectable } from "@angular/core";
import { AuthRepository } from "../repositories/auth.repository";
import { UseCase } from "../../../base/domain/usecase/use-case";
import { LoginResponse } from "../../data/entities/login-response.entity";



@Injectable({
    providedIn: 'root',
})
export class LoginUseCase implements UseCase<{},LoginResponse>{

    constructor(private authRepository: AuthRepository) { }

    execute(params: {username:string,password:string}): Promise<LoginResponse> {
        return this.authRepository.login(params);
    }
    
}