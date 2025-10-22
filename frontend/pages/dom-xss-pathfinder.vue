<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-red-900/20 via-pink-900/20 to-purple-900/20 p-8 border border-red-500/20 backdrop-blur-sm">
      <div class="absolute inset-0 bg-grid-white/5"></div>
      <div class="relative z-10">
        <div class="flex items-center gap-3 mb-2">
          <div class="p-3 bg-gradient-to-br from-red-500/20 to-pink-500/20 rounded-xl">
            <UIcon name="i-heroicons-bug-ant" class="h-8 w-8 text-red-400" />
          </div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-red-400 via-pink-400 to-purple-400 bg-clip-text text-transparent">
            DOM XSS Pathfinder
          </h1>
        </div>
        <p class="text-gray-300 text-lg">Discover DOM-based XSS vulnerabilities in client-side JavaScript</p>
      </div>
    </div>

    <!-- Input Card -->
    <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50 shadow-xl">
      <div class="space-y-6">
        <UFormGroup label="Target URL" help="URL of the page to analyze for DOM XSS">
          <UInput
            v-model="url"
            placeholder="https://example.com/search?q=test"
            size="xl"
            icon="i-heroicons-link"
            :ui="{ 
              base: 'bg-gray-700/50 border-gray-600 focus:border-red-500 focus:ring-red-500/50',
              icon: { leading: { wrapper: 'text-gray-400' } }
            }"
            @keydown.enter="handleAnalyze"
          />
        </UFormGroup>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="bg-gradient-to-br from-red-900/20 to-pink-900/20 rounded-lg p-4 border border-red-500/20">
            <div class="flex items-start gap-2">
              <UIcon name="i-heroicons-information-circle" class="h-5 w-5 text-red-400 flex-shrink-0 mt-0.5" />
              <div class="text-sm text-gray-300">
                <p class="font-semibold text-red-400 mb-1">DOM Sources:</p>
                <p class="text-gray-400">location.href, location.search, document.URL, etc.</p>
              </div>
            </div>
          </div>

          <div class="bg-gradient-to-br from-pink-900/20 to-purple-900/20 rounded-lg p-4 border border-pink-500/20">
            <div class="flex items-start gap-2">
              <UIcon name="i-heroicons-exclamation-triangle" class="h-5 w-5 text-pink-400 flex-shrink-0 mt-0.5" />
              <div class="text-sm text-gray-300">
                <p class="font-semibold text-pink-400 mb-1">DOM Sinks:</p>
                <p class="text-gray-400">eval(), innerHTML, document.write, etc.</p>
              </div>
            </div>
          </div>
        </div>

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
            icon="i-heroicons-magnifying-glass-circle"
            color="red"
            size="lg"
            :loading="isLoading"
            :disabled="!url.trim() || isLoading"
            @click="handleAnalyze"
            class="shadow-lg shadow-red-500/25 hover:shadow-xl hover:shadow-red-500/40 transition-all hover:scale-105"
          >
            Find DOM XSS
          </UButton>
        </div>
      </div>
    </UCard>

    <!-- Loading State -->
    <UCard 
      v-if="isLoading" 
      class="bg-gradient-to-br from-red-900/20 to-pink-900/20 backdrop-blur-sm border border-red-500/30"
    >
      <div class="flex items-center gap-4 p-4">
        <div class="relative">
          <div class="w-12 h-12 border-4 border-red-500/20 border-t-red-500 rounded-full animate-spin"></div>
          <UIcon name="i-heroicons-bug-ant" class="h-6 w-6 text-red-400 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
        </div>
        <div class="flex-1">
          <h3 class="font-bold text-lg text-white">Analyzing DOM Flow...</h3>
          <p class="text-sm text-gray-400 mt-1">Tracing sources to sinks...</p>
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
      <!-- Summary -->
      <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50 shadow-xl">
        <template #header>
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <UIcon name="i-heroicons-chart-bar" class="h-5 w-5 text-red-400" />
              <h2 class="text-lg font-bold bg-gradient-to-r from-red-400 to-pink-400 bg-clip-text text-transparent">
                DOM XSS Analysis
              </h2>
            </div>
            <div class="flex gap-2">
              <UBadge color="red" size="lg">{{ report.analyzedTarget }}</UBadge>
              <UBadge color="gray" size="lg">{{ report.vulnerabilities?.length || 0 }} paths found</UBadge>
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
            <UIcon name="i-heroicons-shield-check" class="h-12 w-12 text-green-400" />
          </div>
          <p class="text-xl font-bold text-green-300">No DOM XSS Vulnerabilities Found!</p>
          <p class="text-green-400/80 mt-2">The application appears to be safe from DOM-based XSS attacks.</p>
        </div>
      </UCard>

      <!-- Source to Sink Flow Visualization -->
      <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50 shadow-xl">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-arrows-right-left" class="h-5 w-5 text-purple-400" />
            <h3 class="font-bold">Data Flow Analysis</h3>
          </div>
        </template>

        <div class="space-y-4">
          <div 
            v-for="(flow, index) in dataFlows" 
            :key="index"
            class="p-4 bg-gray-700/30 rounded-lg border border-gray-600/50 hover:border-purple-500/50 transition-colors"
          >
            <div class="flex items-center gap-2 mb-2">
              <UBadge color="purple" size="xs">Source</UBadge>
              <code class="text-sm text-purple-400 font-mono">{{ flow.source }}</code>
            </div>
            <div class="flex items-center gap-2 ml-4">
              <UIcon name="i-heroicons-arrow-down" class="h-4 w-4 text-gray-500" />
            </div>
            <div class="flex items-center gap-2 ml-4">
              <UBadge color="red" size="xs">Sink</UBadge>
              <code class="text-sm text-red-400 font-mono">{{ flow.sink }}</code>
            </div>
          </div>
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
const report = ref(null);
const dataFlows = ref([]);
const isApiKeyWarningOpen = ref(false);

const resetForm = () => {
  url.value = '';
  error.value = null;
  report.value = null;
  dataFlows.value = [];
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
  report.value = null;
  dataFlows.value = [];
  
  try {
    // Note: The backend expects 'code' parameter, but we're analyzing a URL
    // We'll need to fetch the JavaScript from the URL first, or the backend should handle URL fetching
    // For now, we'll pass the URL as a placeholder and let the backend handle it
    const result = await vulnerabilityService.analyzeDomXss(url.value);
    
    // Format the response
    report.value = {
      id: result.id,
      analyzedTarget: result.analyzed_code || url.value,
      createdAt: result.created_at || new Date().toISOString(),
      vulnerabilities: []
    };
    
    // Transform connected_paths to vulnerabilities
    if (result.connected_paths && result.connected_paths.length > 0) {
      result.connected_paths.forEach(path => {
        report.value.vulnerabilities.push({
          vulnerability: `DOM XSS: ${path.source} → ${path.sink}`,
          severity: 'High',
          description: path.explanation || 'User input flows from a DOM source to a dangerous sink without proper sanitization.',
          impact: 'Attackers can execute arbitrary JavaScript in the context of the victim\'s browser.',
          recommendation: 'Sanitize all user input before using it in dangerous sinks. Use textContent instead of innerHTML where possible.',
          vulnerableCode: path.code_snippet || '',
          injectionPoint: { type: 'DOM', parameter: path.source, method: 'GET' }
        });
      });
      
      // Build data flows from connected paths
      dataFlows.value = result.connected_paths.map(path => ({
        source: path.source,
        sink: path.sink
      }));
    }
    
    // Handle unconnected findings as informational
    if (result.unconnected_findings && result.unconnected_findings.length > 0) {
      const sources = result.unconnected_findings.filter(f => f.type === 'source').map(f => f.value);
      const sinks = result.unconnected_findings.filter(f => f.type === 'sink').map(f => f.value);
      
      if (sources.length > 0 || sinks.length > 0) {
        report.value.vulnerabilities.push({
          vulnerability: 'Potential DOM XSS Indicators',
          severity: 'Info',
          description: `Found ${sources.length} source(s) and ${sinks.length} sink(s) that are not connected. Further investigation recommended.`,
          impact: 'These may not be exploitable on their own but indicate areas for manual testing.',
          recommendation: 'Review the code manually to determine if any paths exist between sources and sinks.',
          vulnerableCode: `Sources: ${sources.join(', ')}\nSinks: ${sinks.join(', ')}`,
          injectionPoint: null
        });
      }
    }
  } catch (e) {
    console.error('DOM XSS analysis error:', e);
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
