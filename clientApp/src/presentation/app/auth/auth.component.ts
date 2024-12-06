import { Component, inject } from "@angular/core";
import { MatSnackBar } from "@angular/material/snack-bar";
import { PatientLoginUseCase } from "../../../domain/usecases/patient-login.usecase";
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from "@angular/forms";

@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrl: './auth.component.css',
  imports:[ReactiveFormsModule]
})
export class AuthComponent {
     private snackBar = inject(MatSnackBar); 
  private loginUseCase = inject(PatientLoginUseCase); 

   authForm: FormGroup;

  constructor() {
    this.authForm = new FormGroup({
      username: new FormControl('', [Validators.required]),
      email: new FormControl('', [Validators.required, Validators.email]),
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

