import { defineStore } from 'pinia';

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    apiKey: '',
    saveApiKey: false,
    disclaimerAccepted: false,
  }),
  
  actions: {
    initialize() {
      // Load settings from localStorage if available
      if (process.client) {
        const savedApiKey = localStorage.getItem('apiKey');
        if (savedApiKey) {
          this.apiKey = savedApiKey;
          this.saveApiKey = true;
        }
        
        const disclaimerAccepted = sessionStorage.getItem('disclaimerAccepted');
        if (disclaimerAccepted === 'true') {
          this.disclaimerAccepted = true;
        }
      }
    },
    
    setApiKey(apiKey: string, saveApiKey: boolean) {
      this.apiKey = apiKey;
      this.saveApiKey = saveApiKey;
      
      if (process.client) {
        if (saveApiKey) {
          localStorage.setItem('apiKey', apiKey);
        } else {
          localStorage.removeItem('apiKey');
        }
      }
    },
    
    acceptDisclaimer() {
      this.disclaimerAccepted = true;
      
      if (process.client) {
        sessionStorage.setItem('disclaimerAccepted', 'true');
      }
    },
    
    rejectDisclaimer() {
      this.disclaimerAccepted = false;
    }
  },
  
  getters: {
    isApiKeySet(): boolean {
      return !!this.apiKey;
    },
    
    hasAcceptedDisclaimer(): boolean {
      return this.disclaimerAccepted;
    }
  }
});
