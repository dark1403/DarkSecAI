<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-indigo-900/20 via-blue-900/20 to-cyan-900/20 p-8 border border-indigo-500/20 backdrop-blur-sm">
      <div class="absolute inset-0 bg-grid-white/5"></div>
      <div class="relative z-10">
        <div class="flex items-center gap-3 mb-2">
          <div class="p-3 bg-gradient-to-br from-indigo-500/20 to-blue-500/20 rounded-xl">
            <UIcon name="i-heroicons-globe-alt" class="h-8 w-8 text-indigo-400" />
          </div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-indigo-400 via-blue-400 to-cyan-400 bg-clip-text text-transparent">
            Discovery Tools
          </h1>
        </div>
        <p class="text-gray-300 text-lg">Discover hidden endpoints, subdomains, and resources</p>
      </div>
    </div>

    <!-- Tabs Card -->
    <!-- <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50 shadow-xl">
      <UTabs :items="tabs" :ui="{ list: { background: 'bg-gray-700/30', marker: { background: 'bg-gradient-to-r from-indigo-500 to-blue-500' } } }">
        <template #default="{ item, selected }">
          <div v-if="selected" class="py-6 mt-4">
            <component :is="item.component" />
          </div>
        </template>
      </UTabs>
    </UCard> -->
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

const UrlListFinder = defineAsyncComponent(() => import('~/components/UrlListFinder.vue'));
const SubdomainFinder = defineAsyncComponent(() => import('~/components/SubdomainFinder.vue'));
const route = useRoute();
const initialPayload = ref('');
const activeTab = ref(0);

const tabs = [
  {
    label: 'URL List Finder',
    icon: 'i-heroicons-map',
    component: markRaw(UrlListFinder),
    description: 'Discover known URLs for a target domain'
  },
  {
    label: 'Subdomain Finder',
    icon: 'i-heroicons-globe-alt',
    component: markRaw(SubdomainFinder),
    description: 'Find subdomains using certificate transparency logs'
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