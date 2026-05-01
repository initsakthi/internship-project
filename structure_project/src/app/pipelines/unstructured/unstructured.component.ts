import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ExtractionService } from '../../services/extraction.service';

@Component({
  selector: 'app-unstructured',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './unstructured.component.html',
  styleUrls: ['./unstructured.component.css']
})
export class UnstructuredComponent {

  availableTags: string[] = [
    'name',
    'email',
    'phone',
    'skills',
    'experience',
    'education',
    'location',
    'projects'
  ];

  selectedTags: string[] = [];
  selectedFile: File | null = null;
  extractedRecords: any[] = [];
  loading: boolean = false;

  constructor(
    private extractionService: ExtractionService,
    public router: Router
  ) {}

  addTag(tag: string): void {
    if (!this.selectedTags.includes(tag)) {
      this.selectedTags.push(tag);
    }
  }

  removeTag(tag: string): void {
    this.selectedTags = this.selectedTags.filter(t => t !== tag);
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];
    }
    this.extractedRecords = [];
  }

  runPipeline(): void {

    if (!this.selectedFile || this.selectedTags.length === 0) {
      alert("Please upload a file and select at least one tag.");
      return;
    }

    this.loading = true;
    this.extractedRecords = [];

    this.extractionService
      .extractUnstructured(this.selectedFile, this.selectedTags)
      .subscribe({
        next: (res: any) => {
          console.log(" FULL BACKEND RESPONSE:", res);
          this.extractedRecords = res?.records || [];
          this.loading = false;
        },
        error: (err) => {
          console.error("Pipeline Error:", err);
          alert('Extraction failed. Make sure FastAPI is running.');
          this.extractedRecords = [];
          this.loading = false;
        }
      });
  }
}