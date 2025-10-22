<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-purple-900/20 via-indigo-900/20 to-pink-900/20 p-8 border border-purple-500/20 backdrop-blur-sm">
      <div class="absolute inset-0 bg-grid-white/5"></div>
      <div class="relative z-10">
        <div class="flex items-center gap-3 mb-2">
          <div class="p-3 bg-gradient-to-br from-purple-500/20 to-indigo-500/20 rounded-xl">
            <UIcon name="i-heroicons-chat-bubble-left-right" class="h-8 w-8 text-purple-400" />
          </div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-purple-400 via-indigo-400 to-pink-400 bg-clip-text text-transparent">
            WebSec Agent
          </h1>
        </div>
        <p class="text-gray-300 text-lg">Expert AI assistant for web security questions and guidance</p>
      </div>
    </div>

    <!-- Chat Card -->
    <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50 shadow-xl">
      <div class="h-[65vh] flex flex-col">
        <div class="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-900/50 rounded-lg mb-4 border border-gray-700/50" ref="messagesEndRef">
          <template v-if="messages.length === 0">
            <div class="text-center p-12 text-gray-400">
              <div class="inline-block p-4 bg-gradient-to-br from-purple-500/20 to-indigo-500/20 rounded-full mb-4">
                <UIcon name="i-heroicons-chat-bubble-left-right" class="h-16 w-16 text-purple-400" />
              </div>
              <p class="text-xl font-medium text-white mb-2">Welcome to WebSec Agent</p>
              <p class="text-lg mb-4">Your AI-powered web security expert</p>
              <div class="text-left max-w-md mx-auto bg-gray-800/50 rounded-lg p-4 border border-purple-500/20">
                <p class="text-sm font-semibold text-purple-400 mb-2">Ask me about:</p>
                <ul class="list-disc list-inside space-y-1 text-sm text-gray-400">
                  <li>Security concepts and techniques</li>
                  <li>Vulnerability exploitation</li>
                  <li>Secure coding practices</li>
                  <li>Tool usage and methodology</li>
                </ul>
              </div>
            </div>
          </template>
          
          <div v-for="(message, index) in messages" :key="index" class="flex">
            <div
              :class="[
                message.role === 'user' 
                  ? 'ml-auto bg-gradient-to-r from-purple-600 to-indigo-600 shadow-lg shadow-purple-500/20' 
                  : 'bg-gray-700/80 shadow-lg',
                'rounded-lg px-4 py-3 max-w-[80%] backdrop-blur-sm'
              ]"
            >
              <div v-if="message.role === 'model' && message.isLoading" class="flex items-center space-x-2">
                <div class="w-2 h-2 rounded-full bg-purple-400 animate-pulse"></div>
                <div class="w-2 h-2 rounded-full bg-indigo-400 animate-pulse" style="animation-delay: 0.2s"></div>
                <div class="w-2 h-2 rounded-full bg-pink-400 animate-pulse" style="animation-delay: 0.4s"></div>
              </div>
              <div v-else class="prose prose-invert max-w-none">
                <MarkdownRenderer :content="message.content" />
              </div>
            </div>
          </div>
        </div>
        
        <div class="flex gap-3">
          <UTextarea
            v-model="userMessage"
            placeholder="Ask a web security question..."
            :rows="2"
            autoresize
            class="flex-1"
            :ui="{ base: 'bg-gray-700/50 border-gray-600 focus:border-purple-500 focus:ring-purple-500/50 backdrop-blur-sm' }"
            @keydown.enter.exact.prevent="sendMessage"
          />
          
          <UButton
            icon="i-heroicons-paper-airplane"
            color="purple"
            size="lg"
            :loading="isLoading"
            :disabled="!userMessage.trim() || isLoading"
            @click="sendMessage"
            class="shadow-lg shadow-purple-500/25 hover:shadow-xl hover:shadow-purple-500/40 transition-all"
          />
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
import chatService from '~/services/api/chatService';

definePageMeta({
  middleware: ['auth']
});

const settingsStore = useSettingsStore();
const userMessage = ref('');
const messages = ref([]);
const isLoading = ref(false);
const isApiKeyWarningOpen = ref(false);
const conversationId = ref(null);
const toast = useToast();
const messagesEndRef = ref(null);

const route = useRoute();
onMounted(() => {
  settingsStore.initialize();
  
  const vulnerability = route.query.vulnerability;
  const targetUrl = route.query.targetUrl;
  
  if (vulnerability && targetUrl) {
    try {
      const vulnObj = JSON.parse(vulnerability);
      const initialMessage = `I found a ${vulnObj.severity.toLowerCase()} severity "${vulnObj.vulnerability}" vulnerability in ${targetUrl}. Can you help me understand this vulnerability better and provide more details on how to exploit and fix it?`;
      userMessage.value = initialMessage;
    } catch (e) {
      console.error('Failed to parse vulnerability from URL', e);
    }
  }
});

// Scroll to bottom when new messages arrive
watch(messages, () => {
  nextTick(() => {
    if (messagesEndRef.value) {
      messagesEndRef.value.scrollIntoView({ behavior: 'smooth' });
    }
  });
}, { deep: true });

const sendMessage = async () => {
  if (!settingsStore.isApiKeySet) {
    isApiKeyWarningOpen.value = true;
    return;
  }
  
  if (!userMessage.value.trim()) return;
  
  // Add user message to UI
  messages.value.push({
    role: 'user',
    content: userMessage.value
  });
  
  // Add loading indicator
  messages.value.push({
    role: 'model',
    content: '',
    isLoading: true
  });
  
  isLoading.value = true;
  const messageToSend = userMessage.value;
  userMessage.value = '';
  
  try {
    // Call the actual chat API
    const response = await chatService.sendMessage({
      conversationId: conversationId.value,
      message: messageToSend
    });
    
    // Update conversation ID if this is the first message
    if (!conversationId.value) {
      conversationId.value = response.conversationId;
    }
    
    // Remove loading indicator and add actual response
    messages.value.pop();
    messages.value.push({
      role: 'model',
      content: response.message
    });
  } catch (error) {
    console.error('Error sending message:', error);
    
    // Remove loading indicator and show error
    messages.value.pop();
    messages.value.push({
      role: 'model',
      content: "Sorry, I encountered an error while processing your request. Please try again."
    });
    
    toast.add({
      title: 'Error',
      description: 'Failed to send message. Please check your API key in settings.',
      color: 'red',
      icon: 'i-heroicons-exclamation-circle'
    });
  } finally {
    isLoading.value = false;
  }
};

const handleGoToSettings = () => {
  isApiKeyWarningOpen.value = false;
  navigateTo('/settings');
};
</script>