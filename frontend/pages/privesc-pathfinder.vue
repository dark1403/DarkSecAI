<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-purple-900/20 via-pink-900/20 to-red-900/20 p-8 border border-purple-500/20 backdrop-blur-sm">
      <div class="absolute inset-0 bg-grid-white/5"></div>
      <div class="relative z-10">
        <div class="flex items-center gap-3 mb-2">
          <div class="p-3 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-xl">
            <UIcon name="i-heroicons-arrow-trending-up" class="h-8 w-8 text-purple-400" />
          </div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-red-400 bg-clip-text text-transparent">
            PrivEsc Pathfinder
          </h1>
        </div>
        <p class="text-gray-300 text-lg">AI-powered privilege escalation and RCE exploit research assistant</p>
      </div>
    </div>

    <!-- Input Card -->
    <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50 shadow-xl">
      <div class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <UFormGroup label="Technology" help="e.g., WordPress, Joomla, Apache">
            <UInput
              v-model="technology"
              placeholder="Enter technology name"
              size="lg"
              icon="i-heroicons-server"
              :ui="{ 
                base: 'bg-gray-700/50 border-gray-600 focus:border-purple-500 focus:ring-purple-500/50',
                icon: { leading: { wrapper: 'text-gray-400' } }
              }"
            />
          </UFormGroup>
          
          <UFormGroup label="Version" help="e.g., 5.8.2, 2.4.50">
            <UInput
              v-model="version"
              placeholder="Enter version number"
              size="lg"
              icon="i-heroicons-hashtag"
              :ui="{ 
                base: 'bg-gray-700/50 border-gray-600 focus:border-purple-500 focus:ring-purple-500/50',
                icon: { leading: { wrapper: 'text-gray-400' } }
              }"
            />
          </UFormGroup>
        </div>

        <UFormGroup label="Additional Context (Optional)" help="OS, architecture, or specific configuration details">
          <UTextarea
            v-model="context"
            placeholder="e.g., Ubuntu 20.04, x64 architecture..."
            :rows="3"
            :ui="{ base: 'bg-gray-700/50 border-gray-600 focus:border-purple-500 focus:ring-purple-500/50' }"
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
            icon="i-heroicons-magnifying-glass-circle"
            color="purple"
            size="xl"
            :loading="isLoading"
            :disabled="!technology.trim() || !version.trim() || isLoading"
            @click="findExploits"
            class="shadow-lg shadow-purple-500/25 hover:shadow-xl hover:shadow-purple-500/40 transition-all hover:scale-105 px-8"
          >
            Find Exploits
          </UButton>
        </div>
      </div>
    </UCard>

    <!-- Loading State -->
    <UCard 
      v-if="isLoading" 
      class="bg-gradient-to-br from-purple-900/20 to-pink-900/20 backdrop-blur-sm border border-purple-500/30"
    >
      <div class="flex items-center gap-4 p-4">
        <div class="relative">
          <div class="w-12 h-12 border-4 border-purple-500/20 border-t-purple-500 rounded-full animate-spin"></div>
          <UIcon name="i-heroicons-magnifying-glass" class="h-6 w-6 text-purple-400 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
        </div>
        <div class="flex-1">
          <h3 class="font-bold text-lg text-white">Searching Exploits...</h3>
          <p class="text-sm text-gray-400 mt-1">Analyzing {{ technology }} {{ version }} for known vulnerabilities</p>
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
          <h3 class="font-bold text-red-200">Search Failed</h3>
          <p class="text-red-300 mt-1">{{ error }}</p>
        </div>
      </div>
    </UCard>

    <!-- Results -->
    <UCard 
      v-if="results && !isLoading"
      class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50 shadow-xl"
    >
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-shield-exclamation" class="h-5 w-5 text-purple-400" />
            <h2 class="font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">Exploit Research Results</h2>
          </div>
          <UBadge color="purple" size="lg">{{ technology }} {{ version }}</UBadge>
        </div>
      </template>

      <div class="prose prose-invert max-w-none">
        <MarkdownRenderer :content="results" />
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
            Discuss with WebSec Agent
          </UButton>
        </div>
      </template>
    </UCard>
  </div>
</template>

<script setup>
import { useSettingsStore } from '~/stores/settings';
import { vulnerabilityService } from '~/services/api';

definePageMeta({
  middleware: ['auth']
});

const settingsStore = useSettingsStore();
const technology = ref('');
const version = ref('');
const context = ref('');
const isLoading = ref(false);
const error = ref(null);
const results = ref(null);

const resetForm = () => {
  technology.value = '';
  version.value = '';
  context.value = '';
  error.value = null;
  results.value = null;
};

const findExploits = async () => {
  if (!settingsStore.isApiKeySet) {
    // Show API key warning
    return;
  }
  
  error.value = null;
  isLoading.value = true;
  results.value = null;
  
  try {
    // Call the backend API
    const report = await vulnerabilityService.findPrivescExploits(technology.value, version.value);
    
    // Format the response as markdown
    let markdown = `# Privilege Escalation Research for ${technology.value} ${version.value}\n\n`;
    
    if (report.vulnerabilities && report.vulnerabilities.length > 0) {
      markdown += `## Known Vulnerabilities\n\n`;
      
      report.vulnerabilities.forEach((vuln, index) => {
        markdown += `### ${index + 1}. ${vuln.vulnerability}\n`;
        markdown += `- **Severity**: ${vuln.severity}\n`;
        markdown += `- **Description**: ${vuln.description}\n`;
        markdown += `- **Impact**: ${vuln.impact}\n`;
        markdown += `- **Recommendation**: ${vuln.recommendation}\n\n`;
        
        if (vuln.vulnerable_code) {
          markdown += `**Vulnerable Code/PoC**:\n\`\`\`\n${vuln.vulnerable_code}\n\`\`\`\n\n`;
        }
      });
    } else {
      markdown += `## No Known Vulnerabilities Found\n\n`;
      markdown += `No specific privilege escalation vulnerabilities were found for ${technology.value} ${version.value}.\n\n`;
      markdown += `This doesn't mean the software is secure - it may mean:\n`;
      markdown += `- The version is too new and hasn't been thoroughly tested\n`;
      markdown += `- Vulnerabilities haven't been publicly disclosed yet\n`;
      markdown += `- The AI couldn't find relevant CVE information\n\n`;
    }
    
    if (context.value.trim()) {
      markdown += `## Additional Context\n\n${context.value}\n\n`;
    }
    
    markdown += `## General Privilege Escalation Techniques\n\n`;
    markdown += `1. **Service Misconfiguration** - Check for weak file permissions\n`;
    markdown += `2. **SUID Binaries** - Look for vulnerable setuid executables\n`;
    markdown += `3. **Kernel Exploits** - Research kernel version vulnerabilities\n`;
    markdown += `4. **Sudo Misconfigurations** - Audit sudo permissions\n`;
    markdown += `5. **Cron Jobs** - Check for writable cron jobs\n`;
    markdown += `6. **Path Hijacking** - Exploit misconfigured PATH variables\n\n`;
    
    markdown += `## Recommended Tools\n`;
    markdown += `- LinPEAS / WinPEAS - Automated privilege escalation enumeration\n`;
    markdown += `- GTFOBins - UNIX binaries that can be exploited\n`;
    markdown += `- Exploit-DB - Search for known exploits\n`;
    markdown += `- searchsploit - Local exploit database search\n`;
    
    results.value = markdown;
  } catch (e) {
    console.error('PrivEsc research error:', e);
    error.value = e.response?.data?.error || e.message || 'Failed to find exploits';
  } finally {
    isLoading.value = false;
  }
};

const sendToAgent = () => {
  navigateTo({
    path: '/websec-agent',
    query: { 
      question: `Tell me more about exploits for ${technology.value} ${version.value}`
    }
  });
};

onMounted(() => {
  settingsStore.initialize();
});
</script>