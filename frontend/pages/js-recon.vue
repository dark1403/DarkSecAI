<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-yellow-900/20 via-orange-900/20 to-red-900/20 p-8 border border-yellow-500/20 backdrop-blur-sm">
      <div class="absolute inset-0 bg-grid-white/5"></div>
      <div class="relative z-10">
        <div class="flex items-center gap-3 mb-2">
          <div class="p-3 bg-gradient-to-br from-yellow-500/20 to-orange-500/20 rounded-xl">
            <UIcon name="i-heroicons-magnifying-glass-circle" class="h-8 w-8 text-yellow-400" />
          </div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-yellow-400 via-orange-400 to-red-400 bg-clip-text text-transparent">
            JS Recon
          </h1>
        </div>
        <p class="text-gray-300 text-lg">Analyze JavaScript code to discover endpoints, API calls, and sensitive data</p>
      </div>
    </div>

    <!-- Input Card -->
    <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50 shadow-xl">
      <div class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <UFormGroup label="Analysis Mode">
            <div class="space-y-3">
              <URadio
                v-model="mode"
                value="url"
                label="Analyze from URL"
                help="Fetch and analyze JavaScript from a URL"
              />
              <URadio
                v-model="mode"
                value="code"
                label="Analyze JavaScript Code"
                help="Paste JavaScript code directly"
              />
            </div>
          </UFormGroup>

          <UFormGroup v-if="mode === 'url'" label="Target URL">
            <UInput
              v-model="url"
              placeholder="https://example.com/app.js"
              size="lg"
              icon="i-heroicons-link"
              :ui="{ 
                base: 'bg-gray-700/50 border-gray-600 focus:border-yellow-500 focus:ring-yellow-500/50',
                icon: { leading: { wrapper: 'text-gray-400' } }
              }"
            />
          </UFormGroup>
        </div>

        <UFormGroup v-if="mode === 'code'" label="JavaScript Code">
          <UTextarea
            v-model="jsCode"
            placeholder="Paste your JavaScript code here..."
            :rows="10"
            class="font-mono text-sm"
            :ui="{ 
              base: 'bg-gray-700/50 border-gray-600 focus:border-yellow-500 focus:ring-yellow-500/50'
            }"
          />
        </UFormGroup>

        <div class="bg-gradient-to-br from-yellow-900/20 to-orange-900/20 rounded-lg p-4 border border-yellow-500/20">
          <div class="flex items-start gap-2">
            <UIcon name="i-heroicons-light-bulb" class="h-5 w-5 text-yellow-400 flex-shrink-0 mt-0.5" />
            <div class="text-sm text-gray-300">
              <p class="font-semibold text-yellow-400 mb-1">What will be discovered:</p>
              <ul class="list-disc list-inside space-y-1 text-gray-400">
                <li>API endpoints and routes</li>
                <li>Hidden URLs and parameters</li>
                <li>API keys and secrets</li>
                <li>Internal logic and algorithms</li>
              </ul>
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
            icon="i-heroicons-sparkles"
            color="yellow"
            size="lg"
            :loading="isLoading"
            :disabled="(!url.trim() && !jsCode.trim()) || isLoading"
            @click="handleAnalyze"
            class="shadow-lg shadow-yellow-500/25 hover:shadow-xl hover:shadow-yellow-500/40 transition-all hover:scale-105"
          >
            Start Reconnaissance
          </UButton>
        </div>
      </div>
    </UCard>

    <!-- Loading State -->
    <UCard 
      v-if="isLoading" 
      class="bg-gradient-to-br from-yellow-900/20 to-orange-900/20 backdrop-blur-sm border border-yellow-500/30"
    >
      <div class="flex items-center gap-4 p-4">
        <div class="relative">
          <div class="w-12 h-12 border-4 border-yellow-500/20 border-t-yellow-500 rounded-full animate-spin"></div>
          <UIcon name="i-heroicons-magnifying-glass" class="h-6 w-6 text-yellow-400 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
        </div>
        <div class="flex-1">
          <h3 class="font-bold text-lg text-white">Analyzing JavaScript...</h3>
          <p class="text-sm text-gray-400 mt-1">Discovering endpoints and sensitive data...</p>
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
    <template v-if="results && !isLoading">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Endpoints Found -->
        <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50 shadow-xl">
          <template #header>
            <div class="flex items-center gap-2">
              <UIcon name="i-heroicons-globe-alt" class="h-5 w-5 text-green-400" />
              <h3 class="font-bold">Endpoints Discovered</h3>
              <UBadge color="green">{{ results.endpoints?.length || 0 }}</UBadge>
            </div>
          </template>
          
          <div v-if="results.endpoints && results.endpoints.length > 0" class="space-y-2 max-h-96 overflow-y-auto">
            <div 
              v-for="(endpoint, index) in results.endpoints" 
              :key="index"
              class="p-3 bg-gray-700/50 rounded-lg border border-gray-600/50 hover:border-green-500/50 transition-colors group"
            >
              <div class="flex items-start gap-2">
                <UBadge :color="getMethodColor(endpoint.method)" size="xs">{{ endpoint.method }}</UBadge>
                <code class="text-sm text-green-400 font-mono flex-1 break-all">{{ endpoint.url }}</code>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-8 text-gray-400">
            <UIcon name="i-heroicons-inbox" class="h-12 w-12 mx-auto mb-2 text-gray-500" />
            <p>No endpoints found</p>
          </div>
        </UCard>

        <!-- Secrets Found -->
        <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50 shadow-xl">
          <template #header>
            <div class="flex items-center gap-2">
              <UIcon name="i-heroicons-key" class="h-5 w-5 text-red-400" />
              <h3 class="font-bold">Sensitive Data</h3>
              <UBadge color="red">{{ results.secrets?.length || 0 }}</UBadge>
            </div>
          </template>
          
          <div v-if="results.secrets && results.secrets.length > 0" class="space-y-2 max-h-96 overflow-y-auto">
            <div 
              v-for="(secret, index) in results.secrets" 
              :key="index"
              class="p-3 bg-red-900/20 rounded-lg border border-red-500/30 hover:border-red-500/50 transition-colors"
            >
              <div class="flex items-start justify-between gap-2">
                <div class="flex-1">
                  <UBadge color="red" size="xs" class="mb-2">{{ secret.type }}</UBadge>
                  <code class="text-sm text-red-400 font-mono block break-all">{{ secret.value }}</code>
                </div>
                <UButton 
                  icon="i-heroicons-clipboard-document" 
                  size="xs" 
                  variant="ghost"
                  @click="copyToClipboard(secret.value)"
                />
              </div>
            </div>
          </div>
          <div v-else class="text-center py-8 text-gray-400">
            <UIcon name="i-heroicons-shield-check" class="h-12 w-12 mx-auto mb-2 text-green-500" />
            <p class="text-green-400">No sensitive data found</p>
          </div>
        </UCard>
      </div>
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
const mode = ref('url');
const url = ref('');
const jsCode = ref('');
const isLoading = ref(false);
const error = ref(null);
const results = ref(null);
const isApiKeyWarningOpen = ref(false);

const resetForm = () => {
  url.value = '';
  jsCode.value = '';
  error.value = null;
  results.value = null;
};

const handleAnalyze = async () => {
  if (!settingsStore.isApiKeySet) {
    isApiKeyWarningOpen.value = true;
    return;
  }
  
  error.value = null;
  isLoading.value = true;
  results.value = null;
  
  try {
    let code = jsCode.value;
    
    // If mode is URL, fetch the JavaScript from the URL
    if (mode.value === 'url' && url.value.trim()) {
      // For now, we'll analyze the URL itself
      // In a real scenario, you'd fetch the JS content from the URL first
      code = `// JavaScript fetched from: ${url.value}\n// (URL mode - direct fetch not implemented)`;
    }
    
    if (!code.trim()) {
      error.value = 'Please provide JavaScript code to analyze';
      return;
    }
    
    // Call the backend API
    const report = await vulnerabilityService.analyzeJsCode(code);
    
    // Transform the vulnerabilities into the expected format
    results.value = {
      endpoints: [],
      secrets: []
    };
    
    // Parse vulnerabilities to extract endpoints and secrets
    if (report.vulnerabilities && report.vulnerabilities.length > 0) {
      report.vulnerabilities.forEach(vuln => {
        // Extract information from vulnerability descriptions
        const desc = vuln.description.toLowerCase();
        
        // If vulnerability mentions endpoints or APIs
        if (desc.includes('endpoint') || desc.includes('api') || desc.includes('route')) {
          // Extract potential endpoints from vulnerable_code
          const urlPattern = /['"`]([/][^'"`\s]+)['"`]/g;
          const matches = vuln.vulnerable_code.matchAll(urlPattern);
          for (const match of matches) {
            results.value.endpoints.push({
              method: 'UNKNOWN',
              url: match[1]
            });
          }
        }
        
        // If vulnerability mentions secrets, keys, or tokens
        if (desc.includes('key') || desc.includes('token') || desc.includes('secret') || desc.includes('credential')) {
          results.value.secrets.push({
            type: vuln.vulnerability,
            value: vuln.vulnerable_code.substring(0, 50) + '...'
          });
        }
      });
    }
    
    // Fallback if no structured data was extracted
    if (results.value.endpoints.length === 0 && results.value.secrets.length === 0 && report.vulnerabilities.length > 0) {
      // Show at least the findings as "endpoints" for visibility
      results.value.endpoints = report.vulnerabilities.map(v => ({
        method: 'INFO',
        url: v.vulnerability
      }));
    }
  } catch (e) {
    console.error('JS analysis error:', e);
    error.value = e.response?.data?.error || e.message || 'An unexpected error occurred during analysis.';
  } finally {
    isLoading.value = false;
  }
};

const getMethodColor = (method) => {
  const colors = {
    'GET': 'blue',
    'POST': 'green',
    'PUT': 'yellow',
    'PATCH': 'orange',
    'DELETE': 'red'
  };
  return colors[method] || 'gray';
};

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text);
    // TODO: Show toast notification
  } catch (e) {
    console.error('Failed to copy', e);
  }
};

const handleGoToSettings = () => {
  isApiKeyWarningOpen.value = false;
};

onMounted(() => {
  settingsStore.initialize();
});
</script>
