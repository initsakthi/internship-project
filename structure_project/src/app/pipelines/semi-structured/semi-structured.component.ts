import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DragDropModule, CdkDragDrop, moveItemInArray } from '@angular/cdk/drag-drop';

@Component({
  selector: 'app-semi-structured',
  standalone: true,
  imports: [CommonModule, FormsModule, DragDropModule],
  templateUrl: './semi-structured.component.html',
  styleUrls: ['./semi-structured.component.css']
})
export class SemiStructuredComponent implements OnInit {
  config = {
    sourceType: 'semi-structured',
    db_host: '127.0.0.1',
    db_port: 27017,
    db_name: 'nosql_db',
    tags: [] as string[]
  };

  availableTags = ['employee_id', 'department', 'project', 'skill_set', 'joining_date', 'performance_score'];
  
  // Updated History with your new Enhancement!
  connectionHistory = [
    { port: 27017, db: 'nosql_db' },
    { port: 27017, db: 'secondary_nosql' } 
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

  removeHistory(index: number, event: Event) {
    event.stopPropagation();
    this.connectionHistory.splice(index, 1);
  }

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
    this.results = []; // Clear old results when switching DBs
  }

  performExtraction() {
    this.loading = true;
    this.http.post('http://localhost:8000/extract', this.config).subscribe({
      next: (res: any) => {
        if (res.status === 'success') {
          this.results = res.records;
        } else {
          alert('Extraction Failed: ' + res.message);
        }
        this.loading = false;
      },
      error: () => {
        alert('Backend unreachable');
        this.loading = false;
      }
    });
  }
}