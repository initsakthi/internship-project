import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
import { provideHttpClient, withFetch } from '@angular/common/http';
import { provideCharts, withDefaultRegisterables } from 'ng2-charts'; // FIXED: Added charting providers

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient(withFetch()),
    // Registers all Chart.js components globally to fix "red error" in component
    provideCharts(withDefaultRegisterables()) 
  ]
};