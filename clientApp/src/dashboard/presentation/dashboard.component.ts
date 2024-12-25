import { Component } from '@angular/core';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent {
  message: string = '';

  // Méthode qui gère la sélection de l'élément
  selectElement(elementNumber: number) {
    this.message = `Bonjour, vous êtes dans l'élément ${elementNumber}`;
  }

  // Méthode pour le bouton "Settings"
  goToSettings() {
    alert('Settings clicked');
  }

  // Méthode pour le bouton "Logout"
  logout() {
    alert('Logout clicked');
  }
}
