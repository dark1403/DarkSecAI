<template>
  <div class="space-y-8">
    <!-- Page Header with Gradient -->
    <div class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-cyan-900/20 via-purple-900/20 to-pink-900/20 p-8 border border-cyan-500/20 backdrop-blur-sm">
      <div class="absolute inset-0 bg-grid-white/5"></div>
      <div class="relative z-10">
        <h1 class="text-4xl font-bold bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
          Dashboard
        </h1>
        <p class="text-gray-300 mt-2 text-lg">Welcome to DarkSec-AI Security Analysis Suite</p>
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <DashboardStatCard
        title="Total Scans"
        :value="dashboardStore.stats.totalScans"
        icon="i-heroicons-chart-bar"
        color="primary"
        :trend="{ isPositive: true, value: '+12%', label: 'from last month' }"
      />
      
      <DashboardStatCard
        title="Vulnerabilities Found"
        :value="dashboardStore.stats.vulnerabilitiesFound"
        icon="i-heroicons-shield-exclamation"
        color="warning"
        :trend="{ isPositive: false, value: '+8%', label: 'from last month' }"
      />
      
      <DashboardStatCard
        title="Critical Issues"
        :value="dashboardStore.stats.criticalIssues"
        icon="i-heroicons-fire"
        color="danger"
      />
      
      <DashboardStatCard
        title="Recent Scans"
        :value="dashboardStore.stats.recentScans"
        icon="i-heroicons-clock"
        color="info"
        :trend="{ isPositive: true, value: '+15', label: 'this week' }"
      />
    </div>

    <!-- Two Column Layout -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Recent Analyses -->
      <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50 shadow-xl">
        <template #header>
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <UIcon name="i-heroicons-clock" class="h-5 w-5 text-cyan-400" />
              <h2 class="text-lg font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">Recent Analyses</h2>
            </div>
            <UButton 
              to="/history"
              variant="ghost"
              color="gray"
              size="xs"
              trailing-icon="i-heroicons-arrow-right"
              class="hover:text-primary transition-colors"
            >
              View All
            </UButton>
          </div>
        </template>
        
        <RecentAnalysisList 
          :analyses="dashboardStore.recentAnalyses.slice(0, 5)"
          @select="handleSelectAnalysis"
        />
      </UCard>

      <!-- Quick Actions -->
      <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50 shadow-xl">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-bolt" class="h-5 w-5 text-purple-400" />
            <h2 class="text-lg font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">Quick Actions</h2>
          </div>
        </template>
        
        <QuickActionsGrid />
      </UCard>
    </div>

    <!-- Vulnerability Distribution -->
    <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50 shadow-xl overflow-hidden">
      <template #header>
        <div class="flex items-center gap-2">
          <UIcon name="i-heroicons-chart-pie" class="h-5 w-5 text-cyan-400" />
          <h2 class="text-lg font-bold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">Vulnerability Overview</h2>
        </div>
      </template>
      
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="text-center p-6 bg-gradient-to-br from-red-900/30 to-red-800/30 rounded-xl border border-red-500/30 backdrop-blur-sm hover:scale-105 transition-transform group">
          <div class="text-5xl font-bold text-red-400 group-hover:text-red-300 transition-colors">{{ criticalCount }}</div>
          <div class="text-sm text-gray-300 mt-2 font-semibold uppercase tracking-wide">Critical</div>
        </div>
        
        <div class="text-center p-6 bg-gradient-to-br from-orange-900/30 to-orange-800/30 rounded-xl border border-orange-500/30 backdrop-blur-sm hover:scale-105 transition-transform group">
          <div class="text-5xl font-bold text-orange-400 group-hover:text-orange-300 transition-colors">{{ highCount }}</div>
          <div class="text-sm text-gray-300 mt-2 font-semibold uppercase tracking-wide">High</div>
        </div>
        
        <div class="text-center p-6 bg-gradient-to-br from-yellow-900/30 to-yellow-800/30 rounded-xl border border-yellow-500/30 backdrop-blur-sm hover:scale-105 transition-transform group">
          <div class="text-5xl font-bold text-yellow-400 group-hover:text-yellow-300 transition-colors">{{ mediumCount }}</div>
          <div class="text-sm text-gray-300 mt-2 font-semibold uppercase tracking-wide">Medium</div>
        </div>
        
        <div class="text-center p-6 bg-gradient-to-br from-green-900/30 to-green-800/30 rounded-xl border border-green-500/30 backdrop-blur-sm hover:scale-105 transition-transform group">
          <div class="text-5xl font-bold text-green-400 group-hover:text-green-300 transition-colors">{{ lowCount }}</div>
          <div class="text-sm text-gray-300 mt-2 font-semibold uppercase tracking-wide">Low</div>
        </div>
      </div>
    </UCard>

    <!-- Getting Started (if no data) -->
    <UCard 
      v-if="!dashboardStore.hasRecentAnalyses"
      class="bg-gradient-to-br from-cyan-900/20 via-purple-900/20 to-pink-900/20 backdrop-blur-sm border border-cyan-500/30 shadow-2xl"
    >
      <template #header>
        <div class="flex items-center gap-2">
          <UIcon name="i-heroicons-rocket-launch" class="h-5 w-5 text-cyan-400" />
          <h2 class="text-lg font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">Getting Started</h2>
        </div>
      </template>
      
      <div class="text-center py-12">
        <div class="inline-block p-4 bg-gradient-to-br from-cyan-500/20 to-purple-500/20 rounded-full mb-6">
          <UIcon name="i-heroicons-rocket-launch" class="h-20 w-20 text-cyan-400" />
        </div>
        <h3 class="text-2xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent mb-3">Welcome to DarkSec-AI!</h3>
        <p class="text-gray-400 mb-8 text-lg">Start by running your first security analysis</p>
        
        <div class="flex gap-4 justify-center">
          <UButton
            to="/url-analysis"
            icon="i-heroicons-link"
            color="cyan"
            size="xl"
            class="shadow-xl shadow-cyan-500/25 hover:shadow-2xl hover:shadow-cyan-500/40 transition-all hover:scale-105"
          >
            Analyze URL
          </UButton>
          
          <UButton
            to="/code-analysis"
            icon="i-heroicons-code-bracket"
            variant="outline"
            size="xl"
            class="border-2 hover:bg-white/5 transition-all hover:scale-105"
          >
            Analyze Code
          </UButton>
        </div>
      </div>
    </UCard>
  </div>
</template>

<script setup>
import { useDashboardStore } from '~/stores/dashboard';

definePageMeta({
  middleware: ['auth']
});

const dashboardStore = useDashboardStore();
const router = useRouter();

// Initialize dashboard data
onMounted(() => {
  dashboardStore.initialize();
  
  // Load mock data if no real data exists (for demo)
  if (!dashboardStore.hasRecentAnalyses) {
    dashboardStore.loadMockData();
  }
});

// Computed severity counts
const criticalCount = computed(() => 
  dashboardStore.recentAnalyses.filter(a => a.severity === 'Critical').length
);

const highCount = computed(() => 
  dashboardStore.recentAnalyses.filter(a => a.severity === 'High').length
);

const mediumCount = computed(() => 
  dashboardStore.recentAnalyses.filter(a => a.severity === 'Medium').length
);

const lowCount = computed(() => 
  dashboardStore.recentAnalyses.filter(a => a.severity === 'Low').length
);

const handleSelectAnalysis = (analysis) => {
  // Navigate to appropriate page based on analysis type
  const routeMap = {
    'url': '/url-analysis',
    'code': '/code-analysis',
    'jwt': '/jwt-analyzer',
    'upload': '/file-upload-auditor',
    'payload': '/payload-tools'
  };
  
  const route = routeMap[analysis.type] || '/history';
  router.push(route);
};
</script>