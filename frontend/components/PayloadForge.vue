<template>
  <div>
    <div class="mb-6">
      <p class="text-sm text-gray-400 mb-4">
        Enter a base payload (e.g., an XSS script), and the AI will generate advanced variations using obfuscation and encoding techniques designed to bypass Web Application Firewalls (WAFs).
      </p>
      
      <UTextarea
        v-model="basePayload"
        placeholder="Enter your base payload here (e.g., &lt;script&gt;alert(1)&lt;/script&gt;)"
        class="font-mono text-sm"
        :rows="3"
      />
      
      <div class="flex justify-center mt-4">
        <UButton
          icon="i-heroicons-fire"
          color="orange"
          :loading="isLoading"
          :disabled="!basePayload.trim() || isLoading"
          @click="generatePayloads"
        >
          Forge Payloads
        </UButton>
      </div>
    </div>
    
    <div v-if="isLoading" class="flex justify-center my-8">
      <UProgress animation="carousel" />
    </div>
    
    <div v-if="error" class="mt-6 p-4 bg-red-900/50 border border-red-700 text-red-200 rounded-lg font-mono">
      {{ error }}
    </div>
    
    <template v-if="payloads.length > 0 && !isLoading">
      <div class="mt-8">
        <h3 class="text-lg font-semibold mb-4">Generated Payloads</h3>
        
        <div class="space-y-4">
          <UCard
            v-for="(payload, index) in payloads"
            :key="index"
            :ui="{ body: { padding: 'p-4' } }"
          >
            <div class="mb-2">
              <span class="font-medium text-cyan-400">{{ payload.technique }}</span>
              <p class="text-sm text-gray-300 mt-1">{{ payload.description }}</p>
            </div>
            
            <div class="bg-gray-800 p-3 rounded-lg font-mono text-sm overflow-x-auto">
              {{ payload.payload }}
            </div>
            
            <div class="flex justify-end mt-4 gap-2">
              <UButton
                icon="i-heroicons-clipboard-document"
                color="gray"
                variant="soft"
                @click="copyToClipboard(payload.payload)"
              >
                Copy
              </UButton>
              <UButton
                icon="i-heroicons-chat-bubble-left-right"
                color="purple"
                variant="soft"
                @click="askAboutPayload(payload)"
              >
                Ask WebSec Agent
              </UButton>
            </div>
          </UCard>
        </div>
      </div>
    </template>
    
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

const props = defineProps({
  initialPayload: {
    type: String,
    default: ''
  }
});

const settingsStore = useSettingsStore();
const basePayload = ref(props.initialPayload);
const isLoading = ref(false);
const error = ref(null);
const payloads = ref([]);
const isApiKeyWarningOpen = ref(false);

// Initialize settings
onMounted(() => {
  settingsStore.initialize();
});

const generatePayloads = async () => {
  if (!settingsStore.isApiKeySet) {
    isApiKeyWarningOpen.value = true;
    return;
  }
  
  if (!basePayload.value.trim()) {
    error.value = 'Please enter a base payload';
    return;
  }
  
  error.value = null;
  isLoading.value = true;
  payloads.value = [];
  
  try {
    // Call the real API
    const result = await vulnerabilityService.forgePayloads(basePayload.value);
    payloads.value = result.payloads;
    
    // Fallback to client-side generation if API returns no payloads
    if (!payloads.value || payloads.value.length === 0) {
      payloads.value = [
        {
          technique: 'HTML Entity Encoding',
          description: 'Replaces characters with their HTML entity equivalents',
          payload: basePayload.value.replace(/</g, '&lt;').replace(/>/g, '&gt;')
        },
        {
          technique: 'JavaScript Unicode Escape',
          description: 'Converts characters to JavaScript Unicode escape sequences',
          payload: Array.from(basePayload.value).map(char => `\\u${char.charCodeAt(0).toString(16).padStart(4, '0')}`).join('')
        },
        {
          technique: 'URL Encoding',
          description: 'Encodes special characters for URL transmission',
          payload: encodeURIComponent(basePayload.value)
        },
        {
          technique: 'Double Encoding',
          description: 'Applies URL encoding twice to bypass certain filters',
          payload: encodeURIComponent(encodeURIComponent(basePayload.value))
        },
        {
          technique: 'Base64 Encoding',
          description: 'Converts payload to Base64 with eval wrapper',
          payload: `eval(atob('${btoa(basePayload.value)}'))`
        }
      ];
    }
  } catch (e) {
    console.error('Error generating payloads:', e);
    error.value = e.response?.data?.error || e.message || 'An unexpected error occurred';
    
    // Fallback to client-side generation if API fails
    payloads.value = [
      {
        technique: 'HTML Entity Encoding',
        description: 'Replaces characters with their HTML entity equivalents',
        payload: basePayload.value.replace(/</g, '&lt;').replace(/>/g, '&gt;')
      },
      {
        technique: 'URL Encoding',
        description: 'Encodes special characters for URL transmission',
        payload: encodeURIComponent(basePayload.value)
      }
    ];
  } finally {
    isLoading.value = false;
  }
};

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text);
    // Could show a toast notification here
  } catch (e) {
    console.error('Failed to copy to clipboard:', e);
  }
};

const askAboutPayload = (payload) => {
  navigateTo({
    path: '/websec-agent',
    query: { 
      message: `Can you explain how this payload works and how it might bypass WAFs? Payload: ${payload.payload}`
    }
  });
};

const handleGoToSettings = () => {
  isApiKeyWarningOpen.value = false;
  // Navigate to settings or open settings modal
};
</script>
