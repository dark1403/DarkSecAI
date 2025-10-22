<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-cyan-900/20 via-blue-900/20 to-indigo-900/20 p-8 border border-cyan-500/20 backdrop-blur-sm">
      <div class="absolute inset-0 bg-grid-white/5"></div>
      <div class="relative z-10">
        <div class="flex items-center gap-3 mb-2">
          <div class="p-3 bg-gradient-to-br from-cyan-500/20 to-blue-500/20 rounded-xl">
            <UIcon name="i-heroicons-link" class="h-8 w-8 text-cyan-400" />
          </div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-cyan-400 via-blue-400 to-indigo-400 bg-clip-text text-transparent">
            URL Analysis (DAST)
          </h1>
        </div>
        <p class="text-gray-300 text-lg">Dynamic Application Security Testing - Analyze URLs for vulnerabilities</p>
      </div>
    </div>

    <!-- Configuration Card -->
    <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50 shadow-xl">
      <div class="space-y-6">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Scan Type -->
          <UFormGroup label="Scan Type">
            <div class="space-y-3">
              <div v-for="option in scanOptions" :key="option.id" class="group">
                <URadio
                  v-model="scanType"
                  :value="option.id"
                  :label="option.name"
                  :help="option.description"
                  class="p-3 rounded-lg hover:bg-gray-700/30 transition-colors border border-transparent hover:border-cyan-500/30"
                />
              </div>
            </div>
          </UFormGroup>

          <!-- Options -->
          <div class="space-y-4">
            <UFormGroup label="Analysis Depth" help="Higher depth = more reliable results">
              <USelect
                v-model="depth"
                :options="depthOptions"
                size="lg"
                :ui="{ 
                  base: 'bg-gray-700/50 border-gray-600 focus:border-cyan-500 focus:ring-cyan-500/50'
                }"
              />
            </UFormGroup>

            <div class="bg-gradient-to-br from-purple-900/20 to-indigo-900/20 rounded-lg p-4 border border-purple-500/20">
              <UCheckbox
                v-model="deepAnalysis"
                label="Enable Deep Analysis"
                help="Performs specialized analysis on each finding (slower, more credits)"
              />
            </div>
            
            <div class="bg-gradient-to-br from-blue-900/20 to-cyan-900/20 rounded-lg p-4 border border-blue-500/20">
              <UCheckbox
                v-model="validateFindings"
                label="Enable Finding Validation"
                help="Filters out AI hallucinations and false positives (recommended)"
              />
            </div>
          </div>
        </div>

        <!-- URL Input -->
        <div class="pt-4 border-t border-gray-700/50">
          <UFormGroup label="Target URL" help="Enter the URL to analyze">
            <div class="flex gap-3">
              <UInput
                v-model="url"
                placeholder="https://example.com"
                size="xl"
                icon="i-heroicons-globe-alt"
                class="flex-1"
                :ui="{ 
                  base: 'bg-gray-700/50 border-gray-600 focus:border-cyan-500 focus:ring-cyan-500/50',
                  icon: { leading: { wrapper: 'text-gray-400' } }
                }"
                @keydown.enter="handleAnalyze"
              />
              
              <UButton
                icon="i-heroicons-magnifying-glass"
                color="cyan"
                size="xl"
                :loading="isLoading"
                :disabled="!url.trim() || isLoading"
                @click="handleAnalyze"
                class="shadow-lg shadow-cyan-500/25 hover:shadow-xl hover:shadow-cyan-500/40 transition-all hover:scale-105 px-8"
              >
                Analyze
              </UButton>
            </div>
          </UFormGroup>
        </div>
      </div>
    </UCard>

    <!-- Loading State -->
    <UCard 
      v-if="isLoading" 
      class="bg-gradient-to-br from-cyan-900/20 to-blue-900/20 backdrop-blur-sm border border-cyan-500/30"
    >
      <div class="p-4">
        <div class="flex items-center gap-4 mb-4">
          <div class="relative">
            <div class="w-12 h-12 border-4 border-cyan-500/20 border-t-cyan-500 rounded-full animate-spin"></div>
            <UIcon name="i-heroicons-command-line" class="h-6 w-6 text-cyan-400 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
          </div>
          <div class="flex-1">
            <h3 class="font-bold text-lg text-white">Analyzing URL...</h3>
            <p class="text-sm text-gray-400 mt-1">Running security analysis</p>
          </div>
        </div>
        
        <div class="bg-gray-900/50 rounded-lg p-4 border border-cyan-500/20">
          <h4 class="text-sm font-semibold text-cyan-400 mb-2 flex items-center gap-2">
            <UIcon name="i-heroicons-terminal" class="h-4 w-4" />
            Live Analysis Log
          </h4>
          <div class="text-sm text-gray-300 space-y-1 font-mono max-h-48 overflow-y-auto">
            <p v-for="(log, index) in analysisLog" :key="index" class="text-green-400">
              <span class="text-cyan-500">></span> {{ log }}
            </p>
          </div>
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
      <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50 shadow-xl">
        <template #header>
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <UIcon name="i-heroicons-document-check" class="h-5 w-5 text-cyan-400" />
              <h2 class="text-lg font-bold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
                Analysis Results
              </h2>
            </div>
            <div class="flex gap-2">
              <UBadge color="cyan" size="lg">{{ report.analyzedTarget }}</UBadge>
              <UBadge color="gray" size="lg">{{ report.vulnerabilities.length }} findings</UBadge>
              <UBadge color="blue" size="lg">{{ new Date(report.createdAt).toLocaleString() }}</UBadge>
            </div>
          </div>
        </template>

        <div v-if="report.vulnerabilities.length > 0" class="space-y-4">
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
            <UIcon name="i-heroicons-shield-check" class="h-12 w-12 text-green-400" />
          </div>
          <p class="text-xl font-bold text-green-300">No Vulnerabilities Found!</p>
          <p class="text-green-400/80 mt-2">The AI did not infer any obvious vulnerabilities for the selected scan type.</p>
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
const scanType = ref('recon');
const depth = ref(3);
const deepAnalysis = ref(false);
const validateFindings = ref(true);
const isLoading = ref(false);
const error = ref(null);
const analysisLog = ref([]);
const report = ref(null);
const isApiKeyWarningOpen = ref(false);

const scanOptions = [
  { id: 'recon', name: 'Recon Scan', description: 'Fast. Uses public intelligence to find vulnerabilities. Low invasiveness.' },
  { id: 'active', name: 'Active Scan', description: 'Thorough. Analyzes inputs and structure to hypothesize vulnerabilities.' },
  { id: 'greybox', name: 'Grey Box Scan', description: 'Most Powerful. Combines Active Scan with JavaScript code analysis.' },
];

const depthOptions = [
  { value: 1, label: '1 (Fastest)' },
  { value: 2, label: '2' },
  { value: 3, label: '3 (Recommended)' },
  { value: 4, label: '4' },
  { value: 5, label: '5 (Most Reliable)' },
];

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
  analysisLog.value = ['Starting Analysis...'];
  report.value = null;
  
  try {
    analysisLog.value.push(`Executing ${scanType.value} scan with depth ${depth.value}...`);
    
    // Call the actual backend API
    const result = await vulnerabilityService.analyzeUrl(url.value);
    
    analysisLog.value.push('Analysis complete. Processing results...');
    
    // Format the response
    report.value = {
      id: result.id,
      analyzedTarget: result.analyzed_target || url.value,
      createdAt: result.created_at || new Date().toISOString(),
      vulnerabilities: result.vulnerabilities || []
    };
    
    analysisLog.value.push(`Found ${report.value.vulnerabilities.length} vulnerabilities.`);
  } catch (e) {
    console.error('URL analysis error:', e);
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