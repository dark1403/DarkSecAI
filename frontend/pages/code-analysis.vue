<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-purple-900/20 via-indigo-900/20 to-blue-900/20 p-8 border border-purple-500/20 backdrop-blur-sm">
      <div class="absolute inset-0 bg-grid-white/5"></div>
      <div class="relative z-10">
        <div class="flex items-center gap-3 mb-2">
          <div class="p-3 bg-gradient-to-br from-purple-500/20 to-indigo-500/20 rounded-xl">
            <UIcon name="i-heroicons-code-bracket" class="h-8 w-8 text-purple-400" />
          </div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-purple-400 via-indigo-400 to-blue-400 bg-clip-text text-transparent">
            Code Analysis (SAST)
          </h1>
        </div>
        <p class="text-gray-300 text-lg">Static Application Security Testing - Analyze source code for vulnerabilities</p>
      </div>
    </div>

    <!-- Configuration & Input Card -->
    <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50 shadow-xl">
      <div class="space-y-6">
        <!-- Analysis Options -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <UFormGroup label="Analysis Depth" help="Higher depth = more reliable results">
            <USelect
              v-model="depth"
              :options="depthOptions"
              size="lg"
              :ui="{ 
                base: 'bg-gray-700/50 border-gray-600 focus:border-purple-500 focus:ring-purple-500/50'
              }"
            />
          </UFormGroup>

          <div class="space-y-3">
            <div class="bg-gradient-to-br from-purple-900/20 to-indigo-900/20 rounded-lg p-4 border border-purple-500/20">
              <UCheckbox
                v-model="deepAnalysis"
                label="Enable Deep Analysis"
                help="Specialized analysis on each finding (slower)"
              />
            </div>
          </div>
        </div>

        <!-- Code Input -->
        <UFormGroup label="Source Code" help="Paste the code you want to analyze">
          <UTextarea
            v-model="code"
            placeholder="Paste your code here (JavaScript, Python, PHP, etc.)..."
            :rows="15"
            class="font-mono text-sm"
            :ui="{ 
              base: 'bg-gray-700/50 border-gray-600 focus:border-purple-500 focus:ring-purple-500/50'
            }"
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
            icon="i-heroicons-sparkles"
            color="purple"
            size="xl"
            :loading="isLoading"
            :disabled="!code.trim() || isLoading"
            @click="handleAnalyze"
            class="shadow-lg shadow-purple-500/25 hover:shadow-xl hover:shadow-purple-500/40 transition-all hover:scale-105 px-8"
          >
            Analyze Code
          </UButton>
        </div>
      </div>
    </UCard>

    <!-- Loading State -->
    <UCard 
      v-if="isLoading" 
      class="bg-gradient-to-br from-purple-900/20 to-indigo-900/20 backdrop-blur-sm border border-purple-500/30"
    >
      <div class="p-4">
        <div class="flex items-center gap-4 mb-4">
          <div class="relative">
            <div class="w-12 h-12 border-4 border-purple-500/20 border-t-purple-500 rounded-full animate-spin"></div>
            <UIcon name="i-heroicons-code-bracket" class="h-6 w-6 text-purple-400 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
          </div>
          <div class="flex-1">
            <h3 class="font-bold text-lg text-white">Analyzing Code...</h3>
            <p class="text-sm text-gray-400 mt-1">Running static analysis</p>
          </div>
        </div>
        
        <div class="bg-gray-900/50 rounded-lg p-4 border border-purple-500/20">
          <h4 class="text-sm font-semibold text-purple-400 mb-2 flex items-center gap-2">
            <UIcon name="i-heroicons-terminal" class="h-4 w-4" />
            Live Analysis Log
          </h4>
          <div class="text-sm text-gray-300 space-y-1 font-mono max-h-48 overflow-y-auto">
            <p v-for="(log, index) in analysisLog" :key="index" class="text-green-400">
              <span class="text-purple-500">></span> {{ log }}
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
              <UIcon name="i-heroicons-document-check" class="h-5 w-5 text-purple-400" />
              <h2 class="text-lg font-bold bg-gradient-to-r from-purple-400 to-indigo-400 bg-clip-text text-transparent">
                Analysis Results
              </h2>
            </div>
            <div class="flex gap-2">
              <UBadge color="purple" size="lg">{{ new Date(report.createdAt).toLocaleString() }}</UBadge>
              <UBadge color="gray" size="lg">{{ report.vulnerabilities.length }} findings</UBadge>
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
            @analyze-with-agent="analyzeWithAgent"
          />
        </div>
        
        <div v-else class="text-center py-12 bg-gradient-to-br from-green-900/20 to-emerald-900/20 rounded-xl border border-green-500/30">
          <div class="inline-block p-4 bg-green-500/20 rounded-full mb-4">
            <UIcon name="i-heroicons-check-badge" class="h-12 w-12 text-green-400" />
          </div>
          <p class="text-xl font-bold text-green-300">Clean Code!</p>
          <p class="text-green-400/80 mt-2">No security vulnerabilities detected in the provided code.</p>
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

const settingsStore = useSettingsStore();
const code = ref('');
const depth = ref(3);
const deepAnalysis = ref(false);
const isLoading = ref(false);
const error = ref(null);
const analysisLog = ref([]);
const report = ref(null);
const isApiKeyWarningOpen = ref(false);

const depthOptions = [
  { value: 1, label: '1 (Fastest)' },
  { value: 2, label: '2' },
  { value: 3, label: '3 (Recommended)' },
  { value: 4, label: '4' },
  { value: 5, label: '5 (Most Reliable)' },
];

const resetForm = () => {
  code.value = '';
  error.value = null;
  report.value = null;
  analysisLog.value = [];
};

const handleAnalyze = async () => {
  if (!settingsStore.isApiKeySet) {
    isApiKeyWarningOpen.value = true;
    return;
  }
  
  if (!code.value.trim()) {
    error.value = 'Please enter code to analyze';
    return;
  }
  
  error.value = null;
  isLoading.value = true;
  analysisLog.value = ['Starting SAST Analysis...'];
  report.value = null;
  
  try {
    analysisLog.value.push(`Analyzing code with depth ${depth.value}...`);
    if (deepAnalysis.value) {
      analysisLog.value.push('Deep analysis enabled for comprehensive scanning...');
    }
    
    // Call the actual backend API
    const result = await vulnerabilityService.analyzeCode(code.value);
    
    analysisLog.value.push('Code analysis complete. Processing results...');
    
    // Format the response
    report.value = {
      id: result.id,
      analyzedTarget: result.analyzed_target || 'Code Analysis',
      createdAt: result.created_at || new Date().toISOString(),
      vulnerabilities: result.vulnerabilities || []
    };
    
    analysisLog.value.push(`Found ${report.value.vulnerabilities.length} security findings.`);
  } catch (e) {
    console.error('Code analysis error:', e);
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

const showExploitAssistant = (vulnerability) => {
  navigateTo({
    path: '/xss-exploit-assistant',
    query: { vulnerability: JSON.stringify(vulnerability) }
  });
};

const analyzeWithAgent = (vulnerability) => {
  navigateTo({
    path: '/websec-agent',
    query: { vulnerability: JSON.stringify(vulnerability) }
  });
};

onMounted(() => {
  settingsStore.initialize();
});
</script>