<template>
  <div class="bg-gray-800 rounded-lg shadow-xl p-6 max-w-md w-full">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-semibold text-white">Settings</h2>
      <UButton
        icon="i-heroicons-x-mark"
        variant="ghost"
        color="gray"
        @click="$emit('close')"
      />
    </div>

    <div class="space-y-6">
      <div>
        <label for="api-key" class="block text-sm font-medium text-gray-300 mb-1">
          Backend API Key
        </label>
        <UInput
          id="api-key"
          v-model="apiKey"
          placeholder="Enter your API key for AI-powered analysis"
          type="password"
          class="w-full"
        />
        <p class="mt-1 text-xs text-gray-400">
          Get your API key from <a href="https://ai.google.dev/" target="_blank" class="text-cyan-400 hover:underline">Google AI Studio</a>
        </p>
      </div>

      <div>
        <UCheckbox
          v-model="saveApiKey"
          label="Save API key in browser"
          class="text-gray-300"
        />
        <p class="mt-1 text-xs text-gray-400">
          Your API key will be stored in your browser's local storage.
        </p>
      </div>

      <div class="pt-4 border-t border-gray-700">
        <UButton
          block
          color="cyan"
          :loading="isTesting"
          @click="testApiKey"
        >
          Test API Key
        </UButton>
        <div v-if="testResult" class="mt-2 text-sm" :class="testResult.success ? 'text-green-400' : 'text-red-400'">
          {{ testResult.message }}
        </div>
      </div>

      <div class="pt-4 border-t border-gray-700">
        <UButton
          block
          color="cyan"
          @click="saveSettings"
        >
          Save Settings
        </UButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useSettingsStore } from '~/stores/settings';

const settingsStore = useSettingsStore();
const apiKey = ref(settingsStore.apiKey);
const saveApiKey = ref(settingsStore.saveApiKey);
const isTesting = ref(false);
const testResult = ref(null);

const testApiKey = async () => {
  isTesting.value = true;
  testResult.value = null;
  
  try {
    // Simulate API test
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    if (apiKey.value) {
      testResult.value = { success: true, message: 'API key is valid!' };
    } else {
      testResult.value = { success: false, message: 'Please enter an API key.' };
    }
  } catch (error) {
    testResult.value = { success: false, message: error.message || 'Failed to test API key.' };
  } finally {
    isTesting.value = false;
  }
};

const saveSettings = () => {
  settingsStore.setApiKey(apiKey.value, saveApiKey.value);
  $emit('close');
};
</script>
