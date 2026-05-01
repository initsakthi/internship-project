import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ExtractionService } from '../services/extraction.service';

@Component({
  selector: 'app-extraction',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './extraction.component.html',
  styleUrls: ['./extraction.component.css']
})
export class ExtractionComponent {
  router = inject(Router);
  
  availableTags = ['name', 'email', 'phone', 'location', 'total_amount', 'invoice_no'];
  selectedTags: string[] = [];
  extractedRecords: any[] = []; // This is the variable the HTML table MUST use
  selectedFile: File | null = null;
  loading: boolean = false;

  constructor(private extractionService: ExtractionService) {}

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  addTag(tag: string) {
    if (!this.selectedTags.includes(tag)) this.selectedTags.push(tag);
  }

  removeTag(tag: string) {
    this.selectedTags = this.selectedTags.filter(t => t !== tag);
  }

  //  This method connects your button to the AI service
  runPipeline() {
    if (!this.selectedFile || this.selectedTags.length === 0) {
      alert("Please select a file and at least one tag.");
      return;
    }

    this.loading = true;
    this.extractedRecords = []; // Clear old UI data

    this.extractionService.extractUnstructured(this.selectedFile, this.selectedTags).subscribe({
      next: (res: any) => {
        console.log("Full JSON from Backend:", res);
        // Backend returns { "status": "success", "records": [...] }
        if (res && res.records) {
          this.extractedRecords = res.records; 
        }
        this.loading = false;
      },
      error: (err) => {
        console.error("Frontend Error:", err);
        this.loading = false;
      }
    });
  }
}