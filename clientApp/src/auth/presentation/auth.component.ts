import { Component, inject } from "@angular/core";
import { MatSnackBar } from "@angular/material/snack-bar";
import { FormBuilder, FormControl, FormGroup, ReactiveFormsModule, Validators } from "@angular/forms";
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { CommonModule } from "@angular/common";
import { LoginUseCase } from "../domain/usecase/login.usecase";

@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrl: './auth.component.css',
  imports:[ReactiveFormsModule, MatFormFieldModule,
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

  constructor(private fb: FormBuilder) { 
    this.authForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });
   }



  async onSubmit() {
    if (this.authForm.valid) {
      const params = {};
    const result = await this.loginUseCase.execute(params);
    console.log(result);
    if (result) {
      this.showToast('login seccess', 'success');
    } else {
      this.showToast('login fail', 'error');
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

