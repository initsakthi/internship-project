import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ExtractionComponent } from './extraction/extraction.component';
import { StructuredComponent } from './pipelines/structured/structured.component';
import { SemiStructuredComponent } from './pipelines/semi-structured/semi-structured.component';
import { UnstructuredComponent } from './pipelines/unstructured/unstructured.component';
// 1. Point this to the new Developer Component
import { DeveloperDashboardComponent } from './developer-dashboard/developer-dashboard.component';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },

  // Role-Based Dashboards: Now using separate components
  { path: 'dashboard', component: DashboardComponent }, 
  { path: 'developer-dashboard', component: DeveloperDashboardComponent }, 

  { path: 'pipeline/structured', component: StructuredComponent },
  { path: 'pipeline/semi-structured', component: SemiStructuredComponent },
  { path: 'pipeline/unstructured', component: UnstructuredComponent },
  { path: 'extraction', component: ExtractionComponent },

  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: '**', redirectTo: '/login' }
];