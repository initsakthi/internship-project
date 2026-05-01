import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username = '';
  password = '';
  role = 'user'; // Bound to the role selection dropdown in your HTML
  isRegisterMode = false;

  constructor(private authService: AuthService, private router: Router) {}

  toggleMode() {
    this.isRegisterMode = !this.isRegisterMode;
    this.username = '';
    this.password = '';
  }

  onLogin() {
    // Sends credentials and selected role to the FastAPI backend
    this.authService.login({ 
      username: this.username, 
      password: this.password,
      role: this.role 
    }).subscribe({
      next: (res: any) => {
        // Persist session data
        localStorage.setItem('role', res.role); 
        localStorage.setItem('username', res.username);
        
        alert(`Authentication Successful. Welcome, ${res.username}!`);

        // ROLE-BASED ROUTING: Physically separates the two user types
        if (res.role === 'developer') {
          // Developers are sent to the technical console
          this.router.navigate(['/developer-dashboard']);
        } else {
          // Standard users are sent to the extraction dashboard
          this.router.navigate(['/dashboard']);
        }
      },
      error: (err) => {
        // Handle mismatched roles or wrong credentials
        const message = err.error?.detail || 'Invalid Credentials or Role Mismatch';
        alert('Login Failed: ' + message);
      }
    });
  }

  onRegister() {
    this.authService.register({ 
      username: this.username, 
      password: this.password, 
      role: this.role 
    }).subscribe({
      next: () => {
        alert('Registration Successful! You can now log in with your assigned role.');
        this.isRegisterMode = false; 
        this.username = ''; 
        this.password = '';
      },
      error: (err) => {
        const message = err.error?.detail || err.message || 'Server Connection Failed';
        alert('Registration Error: ' + message);
      }
    });
  }
}