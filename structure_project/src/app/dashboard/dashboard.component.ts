import { Component, OnInit, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { BaseChartDirective } from 'ng2-charts'; 
import { ChartData } from 'chart.js';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, BaseChartDirective], 
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  username: string = '';
  role: string = ''; // Added to track user role
  isProfileMenuOpen = false;
  networkSpeed = '45 Mbps';
  networkStatusColor = '#22c55e';
  isBrowser: boolean;
  
  // Custom Login Limit Logic
  loginCount = 15; 
  ringColor = '#22c55e'; 

  extractionHistory = [
    { type: 'Structured Pipeline' },
    { type: 'Semi-Structured Pipeline' },
    { type: 'Unstructured Pipeline' },
    { type: 'Structured Pipeline' }
  ];

  public multiRingOptions: any = {
    responsive: true,
    maintainAspectRatio: false,
    cutout: 75,
    plugins: { legend: { display: false } }
  };

  public loginRingData: ChartData<'doughnut'> = {
    labels: ['Used', 'Remaining'],
    datasets: [{
      data: [this.loginCount, 50 - this.loginCount],
      backgroundColor: [this.ringColor, '#f1f5f9'],
      borderWidth: 0,
      borderRadius: 15,
    }]
  };

  constructor(
    public router: Router,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    this.isBrowser = isPlatformBrowser(this.platformId);
  }

  ngOnInit() {
    if (this.isBrowser) {
      this.username = localStorage.getItem('username') || '';
      this.role = localStorage.getItem('role') || ''; // Retrieve role from storage

      // 1. Session Protection: If no username, go to login
      if (!this.username) {
        this.router.navigate(['/login']);
        return;
      }

      // 2. Role-Based Navigation Logic
      // If the URL is '/dashboard' but the user is a developer, redirect them
      const currentUrl = this.router.url;
      if (this.role === 'developer' && currentUrl === '/dashboard') {
        this.router.navigate(['/developer-dashboard']);
        return; 
      } 
      // If a standard user tries to access the developer-dashboard URL, redirect them back
      else if (this.role === 'user' && currentUrl === '/developer-dashboard') {
        this.router.navigate(['/dashboard']);
        return;
      }

      this.loginCount = Number(localStorage.getItem('loginCount')) || 0;
      this.updateRingColor();
      this.startNetworkSimulation();
    }
  }

  updateRingColor() {
    // Logic: Green (0-20), Orange (21-40), Red (41-50)
    if (this.loginCount <= 20) this.ringColor = '#22c55e';
    else if (this.loginCount <= 40) this.ringColor = '#f97316';
    else this.ringColor = '#ef4444';

    this.loginRingData.datasets[0].backgroundColor = [this.ringColor, '#f1f5f9'];
  }

  startNetworkSimulation() {
    setInterval(() => {
      const speed = Math.floor(Math.random() * 20 + 35);
      this.networkSpeed = `${speed} Mbps`;
      this.networkStatusColor = speed < 45 ? '#ef4444' : '#22c55e';
    }, 3000);
  }

  logout() {
    if (this.isBrowser) {
      localStorage.clear(); // Clear session data
      this.router.navigate(['/login']);
    }
  }
}