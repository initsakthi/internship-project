import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ExtractionService {
  private apiUrl = 'http://127.0.0.1:8000'; // Ensure this matches your FastAPI port

  constructor(private http: HttpClient) {}

  //  ADD THIS METHOD to fix the red error in your component
  extractUnstructured(file: File, tags: string[]): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('tags', tags.join(',')); // FastAPI expects a comma-separated string

    return this.http.post(`${this.apiUrl}/extract-unstructured`, formData);
  }

  // Your existing database method (keep this as is)
  getExtractedData(tags: string[], host: string, port: string, db: string, source: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/extract`, {
      sourceType: source,
      tags: tags,
      db_host: host,
      db_port: parseInt(port),
      db_name: db
    });
  }
}