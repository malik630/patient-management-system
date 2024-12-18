import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { firstValueFrom } from "rxjs";
import { AuthRepository } from "../../domain/repositories/auth.repository";

@Injectable({
    providedIn: 'root',
})
export class AuthImplementationRepository extends AuthRepository {


    constructor(private http: HttpClient) {
        super();
    }

    

    override login(params: {}): Promise<boolean> {
        return firstValueFrom(
            this.http.post<boolean>('api', {params})    
        );
    }

    
    
}