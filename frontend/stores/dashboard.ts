import { defineStore } from 'pinia';

export const useDashboardStore = defineStore('dashboard', {
  state: () => ({
    stats: {
      totalScans: 0,
      vulnerabilitiesFound: 0,
      criticalIssues: 0,
      recentScans: 0
    },
    recentAnalyses: [] as Array<{
      id: string;
      type: string;
      target: string;
      severity: string;
      vulnerabilitiesCount: number;
      timestamp: string;
    }>,
    loading: false
  }),

  getters: {
    hasRecentAnalyses: (state) => state.recentAnalyses.length > 0,
    
    criticalCount: (state) => 
      state.recentAnalyses.filter(a => a.severity === 'Critical').length,
    
    highCount: (state) => 
      state.recentAnalyses.filter(a => a.severity === 'High').length,
  },

  actions: {
    initialize() {
      // Load from localStorage if available
      const savedStats = localStorage.getItem('dashboard_stats');
      const savedAnalyses = localStorage.getItem('dashboard_recent_analyses');
      
      if (savedStats) {
        try {
          this.stats = JSON.parse(savedStats);
        } catch (e) {
          console.error('Failed to parse saved stats', e);
        }
      }
      
      if (savedAnalyses) {
        try {
          this.recentAnalyses = JSON.parse(savedAnalyses);
        } catch (e) {
          console.error('Failed to parse saved analyses', e);
        }
      }
    },

    addAnalysis(analysis: {
      type: string;
      target: string;
      severity: string;
      vulnerabilitiesCount: number;
    }) {
      const newAnalysis = {
        id: `analysis-${Date.now()}`,
        ...analysis,
        timestamp: new Date().toISOString()
      };

      // Add to beginning of array
      this.recentAnalyses.unshift(newAnalysis);

      // Keep only last 10 analyses
      if (this.recentAnalyses.length > 10) {
        this.recentAnalyses = this.recentAnalyses.slice(0, 10);
      }

      // Update stats
      this.stats.totalScans++;
      this.stats.vulnerabilitiesFound += analysis.vulnerabilitiesCount;
      
      if (analysis.severity === 'Critical') {
        this.stats.criticalIssues++;
      }

      // Update recent scans (last 7 days)
      const sevenDaysAgo = new Date();
      sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
      this.stats.recentScans = this.recentAnalyses.filter(
        a => new Date(a.timestamp) > sevenDaysAgo
      ).length;

      // Persist to localStorage
      this.persist();
    },

    updateStats(newStats: Partial<typeof this.stats>) {
      this.stats = { ...this.stats, ...newStats };
      this.persist();
    },

    clearHistory() {
      this.recentAnalyses = [];
      this.persist();
    },

    persist() {
      localStorage.setItem('dashboard_stats', JSON.stringify(this.stats));
      localStorage.setItem('dashboard_recent_analyses', JSON.stringify(this.recentAnalyses));
    },

    // Mock data for demo purposes
    loadMockData() {
      this.stats = {
        totalScans: 247,
        vulnerabilitiesFound: 1842,
        criticalIssues: 23,
        recentScans: 45
      };

      this.recentAnalyses = [
        {
          id: '1',
          type: 'url',
          target: 'https://example.com',
          severity: 'High',
          vulnerabilitiesCount: 5,
          timestamp: new Date(Date.now() - 1000 * 60 * 30).toISOString()
        },
        {
          id: '2',
          type: 'code',
          target: 'auth.js',
          severity: 'Critical',
          vulnerabilitiesCount: 2,
          timestamp: new Date(Date.now() - 1000 * 60 * 120).toISOString()
        },
        {
          id: '3',
          type: 'jwt',
          target: 'JWT Token Analysis',
          severity: 'Medium',
          vulnerabilitiesCount: 3,
          timestamp: new Date(Date.now() - 1000 * 60 * 60 * 5).toISOString()
        },
        {
          id: '4',
          type: 'url',
          target: 'https://test.example.com',
          severity: 'Low',
          vulnerabilitiesCount: 1,
          timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString()
        },
        {
          id: '5',
          type: 'payload',
          target: 'XSS Payload Generation',
          severity: 'High',
          vulnerabilitiesCount: 4,
          timestamp: new Date(Date.now() - 1000 * 60 * 60 * 48).toISOString()
        }
      ];

      this.persist();
    }
  }
});
