<template>
  <div class="bg-gray-800 rounded-lg shadow-xl p-6 max-w-md w-full">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-semibold text-yellow-400">API Key Required</h2>
      <UButton
        icon="i-heroicons-x-mark"
        variant="ghost"
        color="gray"
        @click="$emit('close')"
      />
    </div>

    <div class="prose prose-invert max-w-none mb-6">
      <p>
        This feature requires a valid API key to function. The backend uses AI models for security analysis.
      </p>
      
      <p>
        Please configure your API key in the settings to continue.
      </p>
    </div>
    
    <div class="flex justify-end">
      <UButton
        color="cyan"
        @click="goToSettings"
      >
        Go to Settings
      </UButton>
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['close', 'goToSettings']);

const goToSettings = () => {
  emit('goToSettings');
};
</script>
