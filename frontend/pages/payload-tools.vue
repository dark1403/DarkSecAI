<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-orange-900/20 via-red-900/20 to-pink-900/20 p-8 border border-orange-500/20 backdrop-blur-sm">
      <div class="absolute inset-0 bg-grid-white/5"></div>
      <div class="relative z-10">
        <div class="flex items-center gap-3 mb-2">
          <div class="p-3 bg-gradient-to-br from-orange-500/20 to-red-500/20 rounded-xl">
            <UIcon name="i-heroicons-beaker" class="h-8 w-8 text-orange-400" />
          </div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-orange-400 via-red-400 to-pink-400 bg-clip-text text-transparent">
            Payload Tools
          </h1>
        </div>
        <p class="text-gray-300 text-lg">Generate advanced security payloads with obfuscation and evasion techniques</p>
      </div>
    </div>

    <!-- Tabs Card (no overlap) -->
    <UCard
      class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50 shadow-xl overflow-visible"
    >
      <!-- Tabs as the card header -->
      <template #header>
        <UTabs
          v-model="activeTab"
          :items="tabs"
          class="relative z-10"
          :ui="{
            list: {
              base: 'relative z-20 flex gap-1 p-1 rounded-xl bg-gray-700/30 border border-gray-700/40',
              marker: { background: 'bg-gradient-to-r from-orange-500 to-red-500' }
            },
            tab: {
              base: 'px-3 py-2 rounded-lg text-sm font-medium',
              active: 'bg-gray-800/80 shadow'
            }
          }"
        />
      </template>

      <!-- Panel area -->
      <div class="relative z-0 mt-2 rounded-xl border border-gray-700/50 bg-gray-800/40 p-4">
        <component
          :is="tabs[activeTab].component"
          :initial-payload="initialPayload"
        />
      </div>
    </UCard>
  </div>
</template>

<script setup>
import { markRaw } from 'vue';

const route = useRoute();
const initialPayload = ref('');
const activeTab = ref(0);

import PayloadForge from '~/components/PayloadForge.vue';
import SstiForge from '~/components/SstiForge.vue';
import OobInteractionHelper from '~/components/OobInteractionHelper.vue';

const tabs = [
  {
    label: 'Payload Forge',
    icon: 'i-heroicons-fire',
    component: markRaw(PayloadForge),
    description: 'Generate advanced payload variations with obfuscation techniques'
  },
  {
    label: 'SSTI Forge',
    icon: 'i-heroicons-puzzle-piece',
    component: markRaw(SstiForge),
    description: 'Create Server-Side Template Injection payloads for various engines'
  },
  {
    label: 'OOB Helper',
    icon: 'i-heroicons-signal',
    component: markRaw(OobInteractionHelper),
    description: 'Generate Out-of-Band payloads for blind vulnerability testing'
  }
];

onMounted(() => {
  if (route.query.payload) {
    initialPayload.value = route.query.payload;
  }
  
  if (route.query.tab) {
    const tabIndex = tabs.findIndex(tab =>
      tab.label.toLowerCase().replace(/\s+/g, '-') === route.query.tab.toLowerCase()
    );
    if (tabIndex !== -1) {
      activeTab.value = tabIndex;
    }
  }
});

watch(activeTab, (newTab) => {
  const tabName = tabs[newTab].label.toLowerCase().replace(/\s+/g, '-');
  const query = { ...route.query, tab: tabName };
  navigateTo({ query }, { replace: true });
});
</script>