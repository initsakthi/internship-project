import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs'; // Added tap to handle side effects

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://127.0.0.1:8000/auth';

  constructor(private http: HttpClient) {}

  login(credentials: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/login`, credentials).pipe(
      tap((response: any) => {
        // Only save to localStorage if the login is successful
        if (response && response.username) {
          localStorage.setItem('username', response.username);
          localStorage.setItem('role', response.role);
          // Store the login count for the single donut ring
          localStorage.setItem('loginCount', response.login_count.toString());
        }
      })
    );
  }

  register(userData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/register`, userData);
  }
}