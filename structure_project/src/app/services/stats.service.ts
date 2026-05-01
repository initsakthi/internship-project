import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class StatsService {
  // Ensure this matches your FastAPI server port (usually 8000)
  private apiUrl = 'http://localhost:8000/auth/user-stats';

  constructor(private http: HttpClient) {}

  getUserStats(): Observable<any> {
    return this.http.get<any>(this.apiUrl);
  }
}