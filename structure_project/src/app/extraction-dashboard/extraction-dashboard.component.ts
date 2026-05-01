import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-extraction-dashboard',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './extraction-dashboard.component.html',
  styleUrls: ['./extraction-dashboard.component.css']
})
export class ExtractionDashboardComponent {
  extractionForm: FormGroup;
  mockResponse: any = null;
  selectedDataType: string | null = null;

  constructor(private fb: FormBuilder) {
    this.extractionForm = this.fb.group({
      tags: [''],
      dataType: ['']
    });

    this.extractionForm.get('dataType')?.valueChanges.subscribe(val => {
      this.selectedDataType = val;
    });
  }

  get dataTypeMessage(): string {
    switch (this.selectedDataType) {
      case 'Structured':
        return 'Structured data will be extracted from a relational database.';
      case 'Semi-Structured':
        return 'Semi-structured data will be processed using rule-assisted extraction.';
      case 'Unstructured':
        return 'Unstructured data will be processed using AI-based NER models.';
      default:
        return '';
    }
  }

  onSubmit() {
    if (this.extractionForm.valid) {
      const formValue = this.extractionForm.value;
      console.log('Entered tags:', formValue.tags);
      console.log('Selected data type:', formValue.dataType);

      // Mock response
      this.mockResponse = {
        status: 'success',
        extractionId: 'EXT-' + Math.floor(Math.random() * 10000),
        extractedData: {
          tags: formValue.tags.split(',').map((t: string) => t.trim()),
          sourceType: formValue.dataType,
          timestamp: new Date().toISOString(),
          confidenceScore: 0.98
        }
      };
    }
  }
}
