import { Component } from '@angular/core';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent {
  message: string = 'Bienvenue sur le tableau de bord';  // Message initial

  // Méthode qui gère la sélection de l'élément
  selectElement(elementNumber: number): void {
    this.message = `Bonjour, vous êtes dans l'élément ${elementNumber}`;  // Mise à jour du message
  }

  // Méthode pour le bouton "Settings"
  goToSettings(): void {
    // Ajoutez ici la logique pour rediriger l'utilisateur vers la page de paramètres
    this.message = 'Redirection vers les paramètres...';
    console.log('Settings clicked');
  }

  // Méthode pour le bouton "Logout"
  logout(): void {
    // Ajoutez ici la logique pour se déconnecter de l'application (par exemple, en redirigeant l'utilisateur)
    this.message = 'Vous êtes déconnecté.';
    console.log('Logout clicked');
  }
}
