import { Component, OnInit, Inject, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { Router } from '@angular/router';
import { BaseChartDirective } from 'ng2-charts';
import { ChartData, ChartOptions } from 'chart.js';
import { StatsService } from '../services/stats.service';

@Component({
  selector: 'app-developer-dashboard',
  standalone: true,
  imports: [CommonModule, BaseChartDirective],
  template: `
    <div class="admin-wrapper" *ngIf="isBrowser">
      <div class="top-header">
        <div class="greeting">
          <p>Welcome back, <span>{{username}}</span> (Developer)</p>
        </div>
        <button class="logout-link" (click)="logout()">Sign Out</button>
      </div>

      <div class="main-content">
        <h1>System <span>Metrics</span></h1>

        <div class="dashboard-grid">
          <div class="white-card shadow-sm chart-card">
            <h3>MongoDB User Distribution</h3>
            <div class="chart-container" *ngIf="userStatsData">
              <canvas baseChart
                [data]="userStatsData"
                [options]="chartOptions"
                [type]="'doughnut'">
              </canvas>
              <div class="chart-center">
                <span class="count">{{totalUsers}}</span>
                <span class="label">Total Users</span>
              </div>
            </div>
          </div>
          
          <div class="white-card shadow-sm stats-card">
             <h3>Live Data Breakdown</h3>
             <div class="stat-row">
                <span class="dot orange"></span> Developers: <strong>{{devCount}}</strong>
             </div>
             <div class="stat-row">
                <span class="dot light"></span> Standard Users: <strong>{{totalUsers - devCount}}</strong>
             </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .admin-wrapper { background: #f8fafc; min-height: 100vh; padding: 40px; font-family: 'Poppins', sans-serif; }
    .top-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
    .greeting span { color: #11ddf0; font-weight: 700; }
    .logout-link { background: none; border: none; color: #ef4444; cursor: pointer; font-weight: 600; font-family: 'Poppins', sans-serif; }

    .dashboard-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
    .white-card { background: white; border-radius: 24px; padding: 35px; border: 1px solid #f1f5f9; box-shadow: 0 10px 30px rgba(0,0,0,0.02); }
    
    .chart-container { height: 300px; position: relative; display: flex; align-items: center; justify-content: center; }
    .chart-center { position: absolute; text-align: center; pointer-events: none; }
    .chart-center .count { font-size: 2.5rem; font-weight: 800; color: #1e293b; display: block; }
    .chart-center .label { font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; }

    .stat-row { padding: 20px 0; border-bottom: 1px solid #f8fafc; display: flex; align-items: center; }
    .stat-row strong { margin-left: auto; font-size: 1.2rem; }
    .dot { width: 10px; height: 10px; border-radius: 50%; margin-right: 15px; }
    .dot.orange { background: #f97316; }
    .dot.light { background: #f1f5f9; border: 1px solid #e2e8f0; }
  `]
})
export class DeveloperDashboardComponent implements OnInit {
  username = '';
  totalUsers = 0;
  devCount = 0;
  isBrowser: boolean;
  public userStatsData!: ChartData<'doughnut'>;

  public chartOptions: ChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } }
  };

  constructor(
    private statsService: StatsService,
    private router: Router, // Ensure Router is injected here
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    this.isBrowser = isPlatformBrowser(this.platformId);
  }

  ngOnInit() {
    if (this.isBrowser) {
      this.username = localStorage.getItem('username') || 'Developer';
      
      // If a non-developer tries to access this page, send them away
      if (localStorage.getItem('role') !== 'developer') {
        this.router.navigate(['/dashboard']);
        return;
      }
      
      this.loadRealTimeStats();
    }
  }

  loadRealTimeStats() {
    this.statsService.getUserStats().subscribe({
      next: (data) => {
        this.totalUsers = data.total;
        this.devCount = data.developers;
        
        this.userStatsData = {
          labels: ['Developers', 'Users'],
          datasets: [{
            data: [this.devCount, this.totalUsers - this.devCount],
            backgroundColor: ['#f97316', '#f1f5f9'], 
            borderWidth: 0,
            borderRadius: 20,
            // @ts-ignore
            cutout: '82%' 
          }]
        };
      }
    });
  }

  // FIXED LOGOUT METHOD
  logout() {
    if (this.isBrowser) {
      localStorage.clear(); // Wipe all session data
      this.router.navigate(['/login']); // Redirect to login page
    }
  }
}