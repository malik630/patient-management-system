import { Injectable } from "@angular/core";
import { AuthRepository } from "../repositories/auth.repository";
import { UseCase } from "../../../base/domain/usecase/use-case";



@Injectable({
    providedIn: 'root',
})
export class LoginUseCase implements UseCase<{},boolean>{

    constructor(private authRepository: AuthRepository) { }

    execute(params: {}): Promise<boolean> {
        return this.authRepository.login(params);
    }
    
}