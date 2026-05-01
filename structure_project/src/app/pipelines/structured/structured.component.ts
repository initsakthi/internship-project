import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DragDropModule, CdkDragDrop, moveItemInArray } from '@angular/cdk/drag-drop';

@Component({
  selector: 'app-structured',
  standalone: true,
  imports: [CommonModule, FormsModule, DragDropModule],
  templateUrl: './structured.component.html',
  styleUrls: ['./structured.component.css']
})
export class StructuredComponent implements OnInit {
  config = {
    sourceType: 'structured',
    db_host: '127.0.0.1',
    db_port: 3307,
    db_name: 'internship_db',
    tags: [] as string[]
  };

  availableTags = ['name', 'email', 'phone', 'address', 'salary', 'pan_card', 'bank_name', 'dob', 'blood_group'];
  
  connectionHistory = [
    { port: 3307, db: 'internship_db' },
    { port: 3308, db: 'secondary_db' }
  ];
  
  loading = false;
  connectionStatus: 'idle' | 'success' | 'failed' = 'idle';
  results: any[] = [];

  constructor(private http: HttpClient, public router: Router) {}

  ngOnInit() {}

  drop(event: CdkDragDrop<string[]>) {
    if (event.previousContainer === event.container) {
      moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
    } else {
      const tag = event.previousContainer.data[event.previousIndex];
      if (!this.config.tags.includes(tag)) {
        this.config.tags.push(tag);
      }
    }
  }

  removeTag(tag: string) {
    this.config.tags = this.config.tags.filter(t => t !== tag);
  }

  // FIXED: Added missing removeHistory function to resolve the NG9 template error
  removeHistory(index: number, event: Event) {
    event.stopPropagation(); // Prevents clicking the 'x' from also selecting the history item
    this.connectionHistory.splice(index, 1);
  }

  // Real connection test against FastAPI
  testConnection() {
    this.loading = true;
    this.connectionStatus = 'idle';
    this.http.post('http://localhost:8000/test-connection', this.config).subscribe({
      next: (res: any) => {
        this.connectionStatus = res.status === 'success' ? 'success' : 'failed';
        this.loading = false;
      },
      error: () => {
        this.connectionStatus = 'failed';
        this.loading = false;
      }
    });
  }

  selectHistory(item: any) {
    this.config.db_port = item.port;
    this.config.db_name = item.db;
    this.connectionStatus = 'idle';
    this.results = [];
  }

  performExtraction() {
    this.loading = true;
    this.http.post('http://localhost:8000/extract', this.config).subscribe({
      next: (res: any) => {
        if (res.status === 'success') {
          this.results = res.records;
        } else {
          alert('Backend Error: ' + res.message);
        }
        this.loading = false;
      },
      error: (err) => {
        alert('Could not connect to backend.');
        this.loading = false;
      }
    });
  }
}