<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-gray-800/40 via-slate-800/40 to-zinc-800/40 p-8 border border-gray-600/20 backdrop-blur-sm">
      <div class="absolute inset-0 bg-grid-white/5"></div>
      <div class="relative z-10">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="p-3 bg-gradient-to-br from-gray-600/20 to-slate-600/20 rounded-xl">
              <UIcon name="i-heroicons-clock" class="h-8 w-8 text-gray-400" />
            </div>
            <div>
              <h1 class="text-3xl font-bold bg-gradient-to-r from-gray-200 via-slate-300 to-zinc-300 bg-clip-text text-transparent">
                Analysis History
              </h1>
              <p class="text-gray-300 text-lg mt-1">View and manage your previous security analysis reports</p>
            </div>
          </div>
          <UButton
            v-if="history.length > 0"
            icon="i-heroicons-trash"
            color="red"
            variant="soft"
            size="lg"
            @click="confirmClearHistory"
            class="hover:scale-105 transition-transform"
          >
            Clear History
          </UButton>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <UCard 
      v-if="isLoading" 
      class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50"
    >
      <div class="flex items-center gap-4 p-8">
        <div class="relative">
          <div class="w-12 h-12 border-4 border-gray-500/20 border-t-gray-400 rounded-full animate-spin"></div>
          <UIcon name="i-heroicons-clock" class="h-6 w-6 text-gray-400 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
        </div>
        <div class="flex-1">
          <h3 class="font-bold text-lg text-white">Loading History...</h3>
          <p class="text-sm text-gray-400 mt-1">Retrieving your previous analysis reports</p>
        </div>
      </div>
    </UCard>

    <!-- Empty State -->
    <UCard 
      v-else-if="history.length === 0"
      class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50 shadow-xl"
    >
      <div class="text-center py-16">
        <div class="inline-block p-4 bg-gray-700/30 rounded-full mb-4">
          <UIcon name="i-heroicons-document-text" class="h-16 w-16 text-gray-500" />
        </div>
        <h3 class="text-2xl font-bold text-white mb-2">No Analysis History</h3>
        <p class="text-gray-400 mb-8">Your analysis history will appear here once you run some scans</p>
        
        <UButton
          to="/url-analysis"
          icon="i-heroicons-rocket-launch"
          color="cyan"
          size="xl"
          class="shadow-lg shadow-cyan-500/25 hover:shadow-xl hover:shadow-cyan-500/40 transition-all hover:scale-105"
        >
          Start Your First Analysis
        </UButton>
      </div>
    </UCard>

    <!-- History List -->
    <div v-else class="space-y-4">
      <UCard
        v-for="report in history"
        :key="report.id"
        class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50 hover:border-cyan-500/30 shadow-lg hover:shadow-xl transition-all cursor-pointer hover:scale-[1.01] group"
        @click="viewReport(report)"
      >
        <div class="flex items-center justify-between p-2">
          <div class="flex-1">
            <div class="flex items-center gap-3 mb-2">
              <div class="p-2 bg-cyan-500/20 rounded-lg group-hover:scale-110 transition-transform">
                <UIcon :name="getTypeIcon(report.type)" class="h-5 w-5 text-cyan-400" />
              </div>
              <h3 class="font-bold text-lg text-white group-hover:text-cyan-400 transition-colors">{{ report.analyzedTarget }}</h3>
            </div>
            <div class="flex items-center gap-3 ml-11">
              <UBadge color="gray" size="sm">
                {{ new Date(report.createdAt).toLocaleString() }}
              </UBadge>
              <UBadge
                v-if="report.vulnerabilities?.length > 0"
                :color="getSeverityColor(getMaxSeverity(report.vulnerabilities))"
                size="sm"
              >
                {{ report.vulnerabilities.length }} findings
              </UBadge>
              <UBadge
                v-else
                color="green"
                size="sm"
              >
                No vulnerabilities
              </UBadge>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <UButton
              icon="i-heroicons-eye"
              variant="ghost"
              color="gray"
              size="sm"
              @click.stop="viewReport(report)"
              class="hover:text-cyan-400 transition-colors"
            />
            <UButton
              icon="i-heroicons-trash"
              variant="ghost"
              color="red"
              size="sm"
              @click.stop="deleteReport(report.id)"
              class="hover:scale-110 transition-transform"
            />
            <UIcon 
              name="i-heroicons-chevron-right" 
              class="h-5 w-5 text-gray-500 group-hover:text-cyan-400 group-hover:translate-x-1 transition-all" 
            />
          </div>
        </div>
      </UCard>
    </div>

    <!-- Confirmation Modal -->
    <UModal v-model="isClearConfirmOpen">
      <UCard class="bg-gray-800 border-gray-700">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-exclamation-triangle" class="h-5 w-5 text-red-500" />
            <h3 class="text-lg font-semibold text-white">Clear History</h3>
          </div>
        </template>
        
        <p class="text-gray-300">Are you sure you want to clear all analysis history? This action cannot be undone.</p>
        
        <template #footer>
          <div class="flex justify-end gap-2">
            <UButton
              variant="outline"
              @click="isClearConfirmOpen = false"
            >
              Cancel
            </UButton>
            <UButton
              color="red"
              @click="clearHistory"
            >
              Clear History
            </UButton>
          </div>
        </template>
      </UCard>
    </UModal>
  </div>
</template>

<script setup>
import { vulnerabilityService } from '~/services/api';

definePageMeta({
  middleware: ['auth']
});

const history = ref([]);
const isLoading = ref(false);
const selectedReportId = ref(null);
const isClearConfirmOpen = ref(false);

onMounted(() => {
  loadHistory();
});

const loadHistory = async () => {
  isLoading.value = true;
  try {
    // Call the actual backend API
    const reports = await vulnerabilityService.getVulnerabilityReports();
    
    // Transform the data to match the expected format
    history.value = reports.map(report => ({
      id: report.id,
      type: determineReportType(report.analyzed_target),
      analyzedTarget: report.analyzed_target,
      createdAt: report.created_at,
      vulnerabilities: report.vulnerabilities || []
    }));
  } catch (error) {
    console.error('Error loading history:', error);
    // On error, keep empty array
    history.value = [];
  } finally {
    isLoading.value = false;
  }
};

const determineReportType = (target) => {
  if (target.startsWith('http://') || target.startsWith('https://')) {
    return 'url';
  } else if (target.includes('.js') || target.includes('.py') || target.includes('.php')) {
    return 'code';
  } else if (target.includes('JWT') || target.includes('eyJ')) {
    return 'jwt';
  } else if (target.toLowerCase().includes('header')) {
    return 'headers';
  }
  return 'analysis';
};

const getTypeIcon = (type) => {
  const icons = {
    'url': 'i-heroicons-link',
    'code': 'i-heroicons-code-bracket',
    'jwt': 'i-heroicons-key',
    'headers': 'i-heroicons-shield-check'
  };
  return icons[type] || 'i-heroicons-document';
};

const getMaxSeverity = (vulnerabilities) => {
  const severities = vulnerabilities.map(v => v.severity);
  if (severities.includes('Critical')) return 'Critical';
  if (severities.includes('High')) return 'High';
  if (severities.includes('Medium')) return 'Medium';
  if (severities.includes('Low')) return 'Low';
  return 'Info';
};

const getSeverityColor = (severity) => {
  const colors = {
    'Critical': 'red',
    'High': 'orange',
    'Medium': 'yellow',
    'Low': 'green',
    'Info': 'blue'
  };
  return colors[severity] || 'gray';
};

const viewReport = (report) => {
  selectedReportId.value = report.id;
  // TODO: Navigate to detailed view or expand
};

const deleteReport = async (id) => {
  try {
    // For now, just remove from local state
    // TODO: Add DELETE endpoint to backend API
    history.value = history.value.filter(r => r.id !== id);
  } catch (error) {
    console.error('Error deleting report:', error);
  }
};

const confirmClearHistory = () => {
  isClearConfirmOpen.value = true;
};

const clearHistory = async () => {
  try {
    // For now, just clear local state
    // TODO: Add bulk DELETE endpoint to backend API
    history.value = [];
    isClearConfirmOpen.value = false;
  } catch (error) {
    console.error('Error clearing history:', error);
  }
};
</script>