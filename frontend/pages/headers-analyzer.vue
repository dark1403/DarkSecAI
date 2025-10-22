<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-blue-900/20 via-indigo-900/20 to-purple-900/20 p-8 border border-blue-500/20 backdrop-blur-sm">
      <div class="absolute inset-0 bg-grid-white/5"></div>
      <div class="relative z-10">
        <div class="flex items-center gap-3 mb-2">
          <div class="p-3 bg-gradient-to-br from-blue-500/20 to-indigo-500/20 rounded-xl">
            <UIcon name="i-heroicons-shield-check" class="h-8 w-8 text-blue-400" />
          </div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400 bg-clip-text text-transparent">
            Headers Analyzer
          </h1>
        </div>
        <p class="text-gray-300 text-lg">Analyze HTTP security headers and identify misconfigurations</p>
      </div>
    </div>

    <!-- Input Card -->
    <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50 shadow-xl">
      <div class="space-y-6">
        <UFormGroup label="Target URL" help="Enter the URL to analyze HTTP headers">
          <UInput
            v-model="url"
            placeholder="https://example.com"
            size="xl"
            icon="i-heroicons-globe-alt"
            :ui="{ 
              base: 'bg-gray-700/50 border-gray-600 focus:border-blue-500 focus:ring-blue-500/50',
              icon: { leading: { wrapper: 'text-gray-400' } }
            }"
            @keydown.enter="handleAnalyze"
          />
        </UFormGroup>

        <div class="flex items-center justify-end gap-3">
          <UButton
            icon="i-heroicons-arrow-path"
            variant="outline"
            size="lg"
            :disabled="isLoading"
            @click="resetForm"
          >
            Reset
          </UButton>
          
          <UButton
            icon="i-heroicons-magnifying-glass"
            color="blue"
            size="lg"
            :loading="isLoading"
            :disabled="!url.trim() || isLoading"
            @click="handleAnalyze"
            class="shadow-lg shadow-blue-500/25 hover:shadow-xl hover:shadow-blue-500/40 transition-all hover:scale-105"
          >
            Analyze Headers
          </UButton>
        </div>
      </div>
    </UCard>

    <!-- Loading State -->
    <UCard 
      v-if="isLoading" 
      class="bg-gradient-to-br from-blue-900/20 to-indigo-900/20 backdrop-blur-sm border border-blue-500/30"
    >
      <div class="flex items-center gap-4 p-4">
        <div class="relative">
          <div class="w-12 h-12 border-4 border-blue-500/20 border-t-blue-500 rounded-full animate-spin"></div>
          <UIcon name="i-heroicons-shield-check" class="h-6 w-6 text-blue-400 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
        </div>
        <div class="flex-1">
          <h3 class="font-bold text-lg text-white">Analyzing Security Headers...</h3>
          <p class="text-sm text-gray-400 mt-1">{{ analysisLog[analysisLog.length - 1] || 'Starting analysis...' }}</p>
        </div>
      </div>
    </UCard>

    <!-- Error State -->
    <UCard 
      v-if="error && !isLoading"
      class="bg-gradient-to-br from-red-900/30 to-red-800/30 border border-red-500/50 backdrop-blur-sm"
    >
      <div class="flex items-start gap-3">
        <UIcon name="i-heroicons-exclamation-triangle" class="h-6 w-6 text-red-400 flex-shrink-0 mt-1" />
        <div>
          <h3 class="font-bold text-red-200">Analysis Failed</h3>
          <p class="text-red-300 mt-1">{{ error }}</p>
        </div>
      </div>
    </UCard>

    <!-- Results -->
    <template v-if="report && !isLoading">
      <!-- Summary Card -->
      <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50 shadow-xl">
        <template #header>
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <UIcon name="i-heroicons-document-check" class="h-5 w-5 text-blue-400" />
              <h2 class="text-lg font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
                Analysis Results
              </h2>
            </div>
            <div class="flex gap-2">
              <UBadge color="blue" size="lg">{{ report.analyzedTarget }}</UBadge>
              <UBadge color="gray" size="lg">{{ report.vulnerabilities?.length || 0 }} findings</UBadge>
            </div>
          </div>
        </template>

        <div v-if="report.vulnerabilities && report.vulnerabilities.length > 0" class="space-y-4">
          <VulnerabilityCard
            v-for="(vuln, index) in report.vulnerabilities"
            :key="index"
            :vulnerability="vuln"
            :analyzed-target="report.analyzedTarget"
            @send-to-payload-forge="sendToPayloadForge"
            @send-to-jwt-analyzer="sendToJwtAnalyzer"
            @show-exploit-assistant="showExploitAssistant"
            @show-sql-exploit-assistant="showSqlExploitAssistant"
            @analyze-with-agent="analyzeWithAgent"
          />
        </div>

        <div v-else class="text-center py-12 bg-gradient-to-br from-green-900/20 to-emerald-900/20 rounded-xl border border-green-500/30">
          <div class="inline-block p-4 bg-green-500/20 rounded-full mb-4">
            <UIcon name="i-heroicons-check-badge" class="h-12 w-12 text-green-400" />
          </div>
          <p class="text-xl font-bold text-green-300">All Security Headers Configured!</p>
          <p class="text-green-400/80 mt-2">No security header misconfigurations detected.</p>
        </div>
      </UCard>
    </template>

    <!-- API Key Warning Modal -->
    <UModal v-model="isApiKeyWarningOpen">
      <ApiKeyWarningModal 
        @close="isApiKeyWarningOpen = false" 
        @go-to-settings="handleGoToSettings" 
      />
    </UModal>
  </div>
</template>

<script setup>
import { useSettingsStore } from '~/stores/settings';
import { vulnerabilityService } from '~/services/api';

definePageMeta({
  middleware: ['auth']
});

const settingsStore = useSettingsStore();
const url = ref('');
const isLoading = ref(false);
const error = ref(null);
const analysisLog = ref([]);
const report = ref(null);
const isApiKeyWarningOpen = ref(false);

const resetForm = () => {
  url.value = '';
  error.value = null;
  report.value = null;
  analysisLog.value = [];
};

const handleAnalyze = async () => {
  if (!settingsStore.isApiKeySet) {
    isApiKeyWarningOpen.value = true;
    return;
  }
  
  if (!url.value.trim().startsWith('http://') && !url.value.trim().startsWith('https://')) {
    error.value = 'Please enter a valid URL starting with http:// or https://';
    return;
  }
  
  error.value = null;
  isLoading.value = true;
  analysisLog.value = ['Fetching HTTP headers...', 'Analyzing security headers...', 'Checking for misconfigurations...'];
  report.value = null;
  
  try {
    // Call the actual backend API
    const result = await vulnerabilityService.analyzeHeaders(url.value);
    
    analysisLog.value.push('Header analysis complete.');
    
    // Transform HeadersReport to VulnerabilityReport format
    report.value = {
      id: result.id,
      analyzedTarget: result.analyzed_url || url.value,
      createdAt: result.created_at || new Date().toISOString(),
      vulnerabilities: []
    };
    
    // Convert findings to vulnerabilities
    if (result.findings && result.findings.length > 0) {
      result.findings.forEach(finding => {
        // Only include findings that are missing or misconfigured
        if (finding.status === 'Missing' || finding.status === 'Present - Misconfigured') {
          report.value.vulnerabilities.push({
            vulnerability: finding.status === 'Missing' ? `Missing ${finding.name} Header` : `Misconfigured ${finding.name} Header`,
            severity: finding.severity,
            description: finding.status === 'Missing' 
              ? `The ${finding.name} security header is not present.`
              : `The ${finding.name} header is present but misconfigured. Current value: ${finding.value || 'N/A'}`,
            impact: finding.recommendation,
            recommendation: finding.recommendation,
            vulnerableCode: finding.value || null,
            injectionPoint: null
          });
        }
      });
    }
    
    // Add overall summary as an Info finding if score is available
    if (result.overall_score && result.summary) {
      report.value.vulnerabilities.unshift({
        vulnerability: `Security Headers Score: ${result.overall_score}`,
        severity: 'Info',
        description: result.summary,
        impact: 'Overall assessment of HTTP security headers configuration.',
        recommendation: 'Review individual findings below for specific improvements.',
        vulnerableCode: null,
        injectionPoint: null
      });
    }
  } catch (e) {
    console.error('Headers analysis error:', e);
    error.value = e.response?.data?.error || e.message || 'An unexpected error occurred during analysis.';
  } finally {
    isLoading.value = false;
  }
};

const handleGoToSettings = () => {
  isApiKeyWarningOpen.value = false;
};

const sendToPayloadForge = (payload) => {
  navigateTo({ path: '/payload-tools', query: { payload } });
};

const sendToJwtAnalyzer = (token) => {
  navigateTo({ path: '/jwt-analyzer', query: { token } });
};

const showExploitAssistant = (vulnerability, targetUrl) => {
  navigateTo({
    path: '/xss-exploit-assistant',
    query: { vulnerability: JSON.stringify(vulnerability), targetUrl }
  });
};

const showSqlExploitAssistant = (vulnerability, targetUrl) => {
  // Future implementation
};

const analyzeWithAgent = (vulnerability, targetUrl) => {
  navigateTo({
    path: '/websec-agent',
    query: { vulnerability: JSON.stringify(vulnerability), targetUrl }
  });
};

onMounted(() => {
  settingsStore.initialize();
});
</script>
