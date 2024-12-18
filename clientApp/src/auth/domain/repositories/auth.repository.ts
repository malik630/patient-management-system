import { Injectable } from '@angular/core';

@Injectable({
    providedIn: 'root',
})
export abstract class AuthRepository {
    abstract login(params: {}): Promise<boolean>;
}