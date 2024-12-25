import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { firstValueFrom } from "rxjs";
import { AuthRepository } from "../../domain/repositories/auth.repository";
import { LoginResponse } from "../entities/login-response.entity";


@Injectable({
    providedIn: 'root',
})
export class AuthImplementationRepository extends AuthRepository {



    constructor(private http: HttpClient) {
        super();
    }

    

    override async login(params: {username:string,password:string}): Promise<LoginResponse> {
        const response = await firstValueFrom(
            this.http.post<LoginResponse>('http://127.0.0.1:8000/api/auth/login_view/', params)    
        );
        localStorage.setItem('token_access', response.tokens.access)
        return response;
    }

    override async logout(params: {}): Promise<string> {
        const response = await firstValueFrom(
            this.http.post<string>('http://127.0.0.1:8000/api/auth/logout_view/', params)    
        );
        localStorage.removeItem('token_access')
        return response;
    }

    override isAuthenticated(): boolean {
        const token = localStorage.getItem('token_access');
        return token !== null;  ;
    }
    
    
}