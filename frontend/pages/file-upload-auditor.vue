<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-green-900/20 via-emerald-900/20 to-teal-900/20 p-8 border border-green-500/20 backdrop-blur-sm">
      <div class="absolute inset-0 bg-grid-white/5"></div>
      <div class="relative z-10">
        <div class="flex items-center gap-3 mb-2">
          <div class="p-3 bg-gradient-to-br from-green-500/20 to-emerald-500/20 rounded-xl">
            <UIcon name="i-heroicons-document-arrow-up" class="h-8 w-8 text-green-400" />
          </div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-green-400 via-emerald-400 to-teal-400 bg-clip-text text-transparent">
            File Upload Auditor
          </h1>
        </div>
        <p class="text-gray-300 text-lg">AI-powered detection of file upload forms and security analysis</p>
      </div>
    </div>

    <!-- Info Card -->
    <UCard class="bg-gradient-to-br from-green-900/10 to-emerald-900/10 backdrop-blur-sm border border-green-500/20">
      <div class="flex items-start gap-3">
        <UIcon name="i-heroicons-information-circle" class="h-5 w-5 text-green-400 flex-shrink-0 mt-0.5" />
        <div class="text-sm text-gray-300">
          <p class="font-semibold text-green-400 mb-1">How it works:</p>
          <p class="text-gray-400">Enter a URL to detect file upload forms and get AI-powered security analysis with manual testing recommendations.</p>
        </div>
      </div>
    </UCard>

    <!-- Analysis Form -->
    <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50 shadow-xl">
      <div class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">
            Target URL
          </label>
          <div class="flex gap-3">
            <UInput
              v-model="url"
              placeholder="https://example.com/upload"
              size="xl"
              class="flex-1"
              :disabled="isAnalyzing"
              :ui="{ base: 'bg-gray-700/50 border-gray-600 focus:border-green-500 focus:ring-green-500/50' }"
              @keydown.enter="analyzeUrl"
            />
            <UButton
              icon="i-heroicons-magnifying-glass"
              color="green"
              size="xl"
              :loading="isAnalyzing"
              :disabled="!url.trim() || isAnalyzing"
              @click="analyzeUrl"
              class="shadow-lg shadow-green-500/25 hover:shadow-xl hover:shadow-green-500/40 transition-all"
            >
              Analyze
            </UButton>
          </div>
        </div>

        <!-- Error Message -->
        <UAlert
          v-if="analysisError"
          color="red"
          variant="soft"
          icon="i-heroicons-exclamation-triangle"
          :title="analysisError"
          @close="analysisError = null"
        />

        <!-- Loading State -->
        <div v-if="isAnalyzing" class="py-12 text-center">
          <div class="inline-block p-4 bg-gradient-to-br from-green-500/20 to-emerald-500/20 rounded-full mb-4 animate-pulse">
            <UIcon name="i-heroicons-document-arrow-up" class="h-16 w-16 text-green-400" />
          </div>
          <h3 class="text-xl font-bold text-white mb-2">Analyzing File Upload Forms...</h3>
          <p class="text-gray-400">AI is detecting and analyzing file upload functionality</p>
        </div>

        <!-- Results -->
        <div v-else-if="analysisResult" class="space-y-6">
          <!-- Status Badge -->
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div v-if="analysisResult.found" class="p-3 bg-green-500/20 rounded-xl">
                <UIcon name="i-heroicons-check-circle" class="h-6 w-6 text-green-400" />
              </div>
              <div v-else class="p-3 bg-gray-500/20 rounded-xl">
                <UIcon name="i-heroicons-x-circle" class="h-6 w-6 text-gray-400" />
              </div>
              <div>
                <h3 class="text-lg font-bold text-white">
                  {{ analysisResult.found ? 'File Upload Forms Detected' : 'No File Upload Forms Found' }}
                </h3>
                <p class="text-sm text-gray-400">{{ analysisResult.analyzed_url }}</p>
              </div>
            </div>
          </div>

          <!-- Description -->
          <div class="p-6 bg-gray-700/30 rounded-xl border border-gray-600/50">
            <div class="flex items-start gap-3 mb-3">
              <UIcon name="i-heroicons-information-circle" class="h-5 w-5 text-green-400 flex-shrink-0 mt-0.5" />
              <h4 class="font-bold text-white">Analysis</h4>
            </div>
            <div class="prose prose-invert max-w-none">
              <MarkdownRenderer :content="analysisResult.description" />
            </div>
          </div>

          <!-- Manual Testing Guide -->
          <div v-if="analysisResult.found && analysisResult.manual_testing_guide" class="p-6 bg-gradient-to-br from-green-900/20 to-emerald-900/20 rounded-xl border border-green-500/20">
            <div class="flex items-start gap-3 mb-3">
              <UIcon name="i-heroicons-beaker" class="h-5 w-5 text-green-400 flex-shrink-0 mt-0.5" />
              <h4 class="font-bold text-white">Manual Testing Guide</h4>
            </div>
            <div class="prose prose-invert max-w-none">
              <MarkdownRenderer :content="analysisResult.manual_testing_guide" />
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex gap-3">
            <UButton
              color="gray"
              variant="soft"
              icon="i-heroicons-arrow-path"
              @click="resetAnalysis"
            >
              New Analysis
            </UButton>
            <UButton
              v-if="analysisResult.found"
              color="green"
              variant="soft"
              icon="i-heroicons-document-duplicate"
              @click="copyToClipboard(analysisResult.manual_testing_guide)"
            >
              Copy Testing Guide
            </UButton>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-12">
          <div class="inline-block p-4 bg-gradient-to-br from-green-500/20 to-emerald-500/20 rounded-full mb-4">
            <UIcon name="i-heroicons-document-arrow-up" class="h-16 w-16 text-green-400" />
          </div>
          <h3 class="text-2xl font-bold text-white mb-2">File Upload Security Auditor</h3>
          <p class="text-gray-400 mb-8">Enter a URL above to detect and analyze file upload functionality</p>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl mx-auto">
            <div class="p-6 bg-gray-700/30 rounded-xl border border-gray-600/50">
              <div class="p-3 bg-green-500/20 rounded-lg inline-block mb-3">
                <UIcon name="i-heroicons-magnifying-glass" class="h-8 w-8 text-green-400" />
              </div>
              <h4 class="font-bold text-lg text-white mb-2">AI Detection</h4>
              <p class="text-sm text-gray-400">Automatically detects file upload forms on the target website</p>
            </div>

            <div class="p-6 bg-gray-700/30 rounded-xl border border-gray-600/50">
              <div class="p-3 bg-emerald-500/20 rounded-lg inline-block mb-3">
                <UIcon name="i-heroicons-beaker" class="h-8 w-8 text-emerald-400" />
              </div>
              <h4 class="font-bold text-lg text-white mb-2">Testing Guide</h4>
              <p class="text-sm text-gray-400">Get detailed manual testing instructions for security audits</p>
            </div>
          </div>
        </div>
      </div>
    </UCard>

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
import vulnerabilityService from '~/services/api/vulnerabilityService';

definePageMeta({
  middleware: ['auth']
});

const settingsStore = useSettingsStore();
const url = ref('');
const isAnalyzing = ref(false);
const analysisError = ref(null);
const analysisResult = ref(null);
const isApiKeyWarningOpen = ref(false);
const toast = useToast();

onMounted(() => {
  settingsStore.initialize();
});

const analyzeUrl = async () => {
  if (!settingsStore.isApiKeySet) {
    isApiKeyWarningOpen.value = true;
    return;
  }

  if (!url.value.trim()) {
    analysisError.value = 'Please enter a URL';
    return;
  }

  // Basic URL validation
  try {
    new URL(url.value);
  } catch (e) {
    analysisError.value = 'Please enter a valid URL (e.g., https://example.com)';
    return;
  }

  analysisError.value = null;
  isAnalyzing.value = true;
  analysisResult.value = null;

  try {
    const result = await vulnerabilityService.analyzeFileUpload(url.value);
    analysisResult.value = result;

    toast.add({
      title: 'Analysis Complete',
      description: result.found ? 'File upload forms detected!' : 'No file upload forms found',
      color: result.found ? 'green' : 'gray',
      icon: result.found ? 'i-heroicons-check-circle' : 'i-heroicons-information-circle'
    });
  } catch (error) {
    console.error('Error analyzing file upload:', error);
    analysisError.value = 'Failed to analyze URL. Please check your API key and try again.';
    
    toast.add({
      title: 'Analysis Failed',
      description: 'Failed to analyze the URL. Please check your API key in settings.',
      color: 'red',
      icon: 'i-heroicons-exclamation-circle'
    });
  } finally {
    isAnalyzing.value = false;
  }
};

const resetAnalysis = () => {
  analysisResult.value = null;
  analysisError.value = null;
  url.value = '';
};

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text);
    toast.add({
      title: 'Copied!',
      description: 'Testing guide copied to clipboard',
      color: 'green',
      icon: 'i-heroicons-check-circle'
    });
  } catch (error) {
    console.error('Failed to copy:', error);
    toast.add({
      title: 'Copy Failed',
      description: 'Failed to copy to clipboard',
      color: 'red',
      icon: 'i-heroicons-exclamation-circle'
    });
  }
};

const handleGoToSettings = () => {
  isApiKeyWarningOpen.value = false;
  navigateTo('/settings');
};
</script>