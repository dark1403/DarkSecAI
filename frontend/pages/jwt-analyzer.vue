<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-yellow-900/20 via-amber-900/20 to-orange-900/20 p-8 border border-yellow-500/20 backdrop-blur-sm">
      <div class="absolute inset-0 bg-grid-white/5"></div>
      <div class="relative z-10">
        <div class="flex items-center gap-3 mb-2">
          <div class="p-3 bg-gradient-to-br from-yellow-500/20 to-amber-500/20 rounded-xl">
            <UIcon name="i-heroicons-key" class="h-8 w-8 text-yellow-400" />
          </div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-yellow-400 via-amber-400 to-orange-400 bg-clip-text text-transparent">
            JWT Analyzer
          </h1>
        </div>
        <p class="text-gray-300 text-lg">Analyze JSON Web Tokens for security vulnerabilities and misconfigurations</p>
      </div>
    </div>

    <!-- Input Card -->
    <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50 shadow-xl">
      <div class="space-y-6">
        <UFormGroup label="JWT Token" help="Paste your JWT token to analyze">
          <UTextarea
            v-model="token"
            placeholder="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            :rows="4"
            class="font-mono text-sm"
            :ui="{ 
              base: 'bg-gray-700/50 border-gray-600 focus:border-yellow-500 focus:ring-yellow-500/50'
            }"
          />
        </UFormGroup>

        <UFormGroup label="Analysis Mode">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div 
              @click="mode = 'blue_team'"
              :class="[
                'p-4 rounded-xl border-2 cursor-pointer transition-all',
                mode === 'blue_team' 
                  ? 'border-blue-500 bg-blue-500/10' 
                  : 'border-gray-600 hover:border-gray-500 bg-gray-700/30'
              ]"
            >
              <div class="flex items-center gap-2 mb-2">
                <UIcon name="i-heroicons-shield-check" class="h-5 w-5 text-blue-400" />
                <span class="font-bold text-white">Blue Team (Defensive)</span>
              </div>
              <p class="text-sm text-gray-400">Check for security best-practice violations</p>
            </div>

            <div 
              @click="mode = 'red_team'"
              :class="[
                'p-4 rounded-xl border-2 cursor-pointer transition-all',
                mode === 'red_team' 
                  ? 'border-red-500 bg-red-500/10' 
                  : 'border-gray-600 hover:border-gray-500 bg-gray-700/30'
              ]"
            >
              <div class="flex items-center gap-2 mb-2">
                <UIcon name="i-heroicons-fire" class="h-5 w-5 text-red-400" />
                <span class="font-bold text-white">Red Team (Offensive)</span>
              </div>
              <p class="text-sm text-gray-400">Look for attack vectors and exploitation opportunities</p>
            </div>
          </div>
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
            icon="i-heroicons-key"
            color="yellow"
            size="xl"
            :loading="isLoading"
            :disabled="!token.trim() || isLoading"
            @click="analyzeToken"
            class="shadow-lg shadow-yellow-500/25 hover:shadow-xl hover:shadow-yellow-500/40 transition-all hover:scale-105 px-8"
          >
            Analyze Token
          </UButton>
        </div>
      </div>
    </UCard>

    <!-- Loading State -->
    <UCard 
      v-if="isLoading" 
      class="bg-gradient-to-br from-yellow-900/20 to-amber-900/20 backdrop-blur-sm border border-yellow-500/30"
    >
      <div class="flex items-center gap-4 p-4">
        <div class="relative">
          <div class="w-12 h-12 border-4 border-yellow-500/20 border-t-yellow-500 rounded-full animate-spin"></div>
          <UIcon name="i-heroicons-key" class="h-6 w-6 text-yellow-400 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
        </div>
        <div class="flex-1">
          <h3 class="font-bold text-lg text-white">Analyzing JWT...</h3>
          <p class="text-sm text-gray-400 mt-1">Decoding and analyzing token security</p>
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

    <!-- Token Parts Display -->
    <template v-if="tokenParts && !isLoading">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50 shadow-xl">
          <template #header>
            <div class="flex items-center gap-2">
              <UIcon name="i-heroicons-document-text" class="h-5 w-5 text-blue-400" />
              <h3 class="font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">Header</h3>
            </div>
          </template>
          <div class="bg-gray-900/80 p-4 rounded-lg border border-gray-700/50">
            <pre class="text-sm text-cyan-300 font-mono overflow-auto">{{ JSON.stringify(tokenParts.header, null, 2) }}</pre>
          </div>
        </UCard>
        
        <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50 shadow-xl">
          <template #header>
            <div class="flex items-center gap-2">
              <UIcon name="i-heroicons-cube" class="h-5 w-5 text-purple-400" />
              <h3 class="font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">Payload</h3>
            </div>
          </template>
          <div class="bg-gray-900/80 p-4 rounded-lg border border-gray-700/50">
            <pre class="text-sm text-purple-300 font-mono overflow-auto">{{ JSON.stringify(tokenParts.payload, null, 2) }}</pre>
          </div>
        </UCard>
      </div>

      <!-- Analysis Results -->
      <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50 shadow-xl">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-document-magnifying-glass" class="h-5 w-5 text-yellow-400" />
            <h3 class="font-bold bg-gradient-to-r from-yellow-400 to-orange-400 bg-clip-text text-transparent">Security Analysis</h3>
          </div>
        </template>
        
        <div v-if="analysis" class="prose prose-invert max-w-none">
          <MarkdownRenderer :content="analysis" />
        </div>
        
        <template #footer>
          <div class="flex justify-end gap-2">
            <UButton
              icon="i-heroicons-chat-bubble-left-right"
              color="purple"
              variant="soft"
              @click="sendToAgent"
              class="hover:scale-105 transition-transform"
            >
              Ask WebSec Agent
            </UButton>
          </div>
        </template>
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
const token = ref('');
const mode = ref('blue_team');
const isLoading = ref(false);
const error = ref(null);
const tokenParts = ref(null);
const analysis = ref(null);
const isApiKeyWarningOpen = ref(false);

const route = useRoute();

onMounted(() => {
  settingsStore.initialize();
  if (route.query.token) {
    token.value = route.query.token;
  }
});

const resetForm = () => {
  token.value = '';
  error.value = null;
  tokenParts.value = null;
  analysis.value = null;
};

const analyzeToken = async () => {
  if (!settingsStore.isApiKeySet) {
    isApiKeyWarningOpen.value = true;
    return;
  }
  
  if (!token.value.trim()) {
    error.value = 'Please paste a JWT token';
    return;
  }
  
  error.value = null;
  isLoading.value = true;
  tokenParts.value = null;
  analysis.value = null;
  
  try {
    // Decode JWT (basic decoding for display)
    const parts = token.value.split('.');
    if (parts.length !== 3) {
      throw new Error('Invalid JWT format. Expected 3 parts separated by dots.');
    }
    
    const header = JSON.parse(atob(parts[0]));
    const payload = JSON.parse(atob(parts[1]));
    
    tokenParts.value = { header, payload };
    
    // Call the actual backend API for security analysis
    const result = await vulnerabilityService.analyzeJwt(token.value);
    
    // Format the analysis as markdown
    let markdown = `## JWT Security Analysis (${mode.value === 'blue_team' ? 'Blue Team' : 'Red Team'} Mode)\n\n`;
    
    if (result.vulnerabilities && result.vulnerabilities.length > 0) {
      result.vulnerabilities.forEach(vuln => {
        markdown += `### ${vuln.vulnerability}\n`;
        markdown += `- **Severity**: ${vuln.severity}\n`;
        markdown += `- **Description**: ${vuln.description}\n`;
        markdown += `- **Impact**: ${vuln.impact}\n`;
        markdown += `- **Recommendation**: ${vuln.recommendation}\n\n`;
        
        if (vuln.vulnerable_code) {
          markdown += `**Details**:\n\`\`\`\n${vuln.vulnerable_code}\n\`\`\`\n\n`;
        }
      });
    } else {
      // Fallback to basic analysis if no vulnerabilities found
      markdown += `### Algorithm\n`;
      markdown += `- **Type**: ${header.alg}\n`;
      markdown += `- **Security**: ${header.alg === 'none' ? '⚠️ CRITICAL - Algorithm set to "none"' : '✅ Algorithm specified'}\n\n`;
      
      markdown += `### Expiration\n`;
      markdown += `- **Status**: ${payload.exp ? `Expires at ${new Date(payload.exp * 1000).toLocaleString()}` : '⚠️ No expiration set'}\n\n`;
      
      markdown += `### Token Structure\n`;
      markdown += `- **Claims**: ${Object.keys(payload).join(', ')}\n\n`;
      
      if (mode.value === 'blue_team') {
        markdown += `### Defensive Recommendations\n`;
        markdown += `- Verify signature on every request\n`;
        markdown += `- Use strong secret keys (256+ bits)\n`;
        markdown += `- Implement proper expiration handling\n`;
        markdown += `- Validate all claims before use\n`;
      } else {
        markdown += `### Offensive Testing Ideas\n`;
        markdown += `- Test algorithm confusion (alg: none)\n`;
        markdown += `- Attempt signature verification bypass\n`;
        markdown += `- Try JWT secret brute-forcing\n`;
        markdown += `- Test for claim injection\n`;
      }
    }
    
    analysis.value = markdown;
  } catch (e) {
    console.error('JWT analysis error:', e);
    error.value = e.response?.data?.error || e.message || 'Failed to analyze JWT token';
  } finally {
    isLoading.value = false;
  }
};

const sendToAgent = () => {
  navigateTo({
    path: '/websec-agent',
    query: { token: token.value }
  });
};

const handleGoToSettings = () => {
  isApiKeyWarningOpen.value = false;
};
</script>