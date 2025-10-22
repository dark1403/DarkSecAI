<template>
  <div class="fixed inset-0 bg-gray-900 bg-opacity-75 flex items-center justify-center p-4 z-50">
    <div class="bg-gray-800 rounded-lg shadow-xl p-6 max-w-lg w-full">
      <h2 class="text-xl font-bold text-white mb-4">Disclaimer</h2>
      
      <div class="prose prose-invert max-w-none mb-6">
        <p>
          This application is provided for <strong>educational and research purposes only</strong>.
        </p>
        
        <p>
          The AI's output may contain inaccuracies, false positives, or false negatives. 
          It is <strong>NOT</strong> a substitute for professional security auditing or manual code review.
        </p>
        
        <p class="text-red-400 font-semibold">
          By using this tool, you acknowledge and agree that you will only test applications 
          for which you have explicit, written permission from the owner.
        </p>
        
        <p>
          The creator of this tool assumes no liability for any misuse or damage caused by this application. 
          Always verify findings manually.
        </p>
      </div>
      
      <div class="flex flex-col sm:flex-row gap-4">
        <UButton
          block
          color="red"
          @click="rejectDisclaimer"
        >
          I Disagree
        </UButton>
        
        <UButton
          block
          color="cyan"
          @click="acceptDisclaimer"
        >
          I Agree
        </UButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useSettingsStore } from '~/stores/settings';

const settingsStore = useSettingsStore();

const acceptDisclaimer = () => {
  settingsStore.acceptDisclaimer();
};

const rejectDisclaimer = () => {
  settingsStore.rejectDisclaimer();
  // Redirect to a rejection page or show a message
  navigateTo('/disclaimer-rejected');
};
</script>
