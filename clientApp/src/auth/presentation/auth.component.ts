import { Component, inject } from "@angular/core";
import { MatSnackBar } from "@angular/material/snack-bar";
import { FormBuilder, FormControl, FormGroup, ReactiveFormsModule, Validators } from "@angular/forms";
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { Router } from '@angular/router';
import { CommonModule } from "@angular/common";
import { LoginUseCase } from "../domain/usecase/login.usecase";
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';

@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrl: './auth.component.css',
  imports:[ReactiveFormsModule, 
    MatFormFieldModule,
    MatProgressSpinnerModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    CommonModule,
    MatCardModule]
  
})
export class AuthComponent {
     private snackBar = inject(MatSnackBar); 
      private loginUseCase = inject(LoginUseCase); 

   authForm: FormGroup;
   hidePassword: boolean = true;
   isLoading = false;

  constructor(private fb: FormBuilder, private router: Router) { 
    this.authForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });
   }



  async onSubmit() {
    if (this.authForm.valid) {
      const params = {username:this.authForm.value.email,password:this.authForm.value.password};
      this.isLoading=true;
    const result = await this.loginUseCase.execute(params);
    console.log(result);
    if (result) {
      this.router.navigate(['/dashboard']);
    } else {
      this.showToast('Invalid credentials. Please try again.', 'error');
    }
    }
  }

   showToast(message: string, type: string): void {
    this.snackBar.open(message, 'Close', {
      duration: 3000,
      panelClass: type === 'success' ? 'success-snackbar' : 'error-snackbar',
    });
  }
}

