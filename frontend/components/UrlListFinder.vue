<template>
  <div>
    <div class="mb-6">
      <p class="text-sm text-gray-400 mb-4">
        Discover all known URLs for a target domain by querying the extensive index of the Wayback Machine.
      </p>
      
      <div class="flex flex-col sm:flex-row gap-4">
        <UInput
          v-model="domain"
          placeholder="Enter domain (e.g., example.com)"
          class="flex-grow"
        />
        
        <UButton
          icon="i-heroicons-magnifying-glass"
          color="cyan"
          :loading="isLoading"
          :disabled="!domain.trim() || isLoading"
          @click="findUrls"
        >
          Find URLs
        </UButton>
      </div>
    </div>
    
    <div v-if="isLoading" class="flex justify-center my-8">
      <UProgress animation="carousel" />
    </div>
    
    <div v-if="error" class="mt-6 p-4 bg-red-900/50 border border-red-700 text-red-200 rounded-lg font-mono">
      {{ error }}
    </div>
    
    <template v-if="urls.length > 0 && !isLoading">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold">Found {{ urls.length }} URLs</h3>
        <div class="flex gap-2">
          <UInput
            v-model="searchTerm"
            placeholder="Filter results..."
            icon="i-heroicons-magnifying-glass"
            size="sm"
          />
          <UButton
            icon="i-heroicons-document-arrow-down"
            color="gray"
            variant="soft"
            @click="downloadResults"
          >
            Export
          </UButton>
        </div>
      </div>
      
      <UCard>
        <div class="max-h-96 overflow-y-auto">
          <table class="w-full">
            <thead class="bg-gray-800 sticky top-0">
              <tr>
                <th class="text-left py-2 px-3 text-sm font-medium text-gray-300">#</th>
                <th class="text-left py-2 px-3 text-sm font-medium text-gray-300">URL</th>
                <th class="text-left py-2 px-3 text-sm font-medium text-gray-300">Last Seen</th>
                <th class="text-right py-2 px-3 text-sm font-medium text-gray-300">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="(url, index) in filteredUrls" 
                :key="index"
                class="border-t border-gray-700 hover:bg-gray-800/50"
              >
                <td class="py-2 px-3 text-sm text-gray-400">{{ index + 1 }}</td>
                <td class="py-2 px-3 text-sm">
                  <div class="flex items-center">
                    <UIcon 
                      :name="getUrlTypeIcon(url.url)" 
                      class="mr-2 text-gray-400 flex-shrink-0"
                    />
                    <span class="truncate max-w-md">{{ url.url }}</span>
                  </div>
                </td>
                <td class="py-2 px-3 text-sm text-gray-400">{{ url.lastSeen }}</td>
                <td class="py-2 px-3 text-right">
                  <div class="flex justify-end gap-1">
                    <UButton
                      icon="i-heroicons-clipboard-document"
                      color="gray"
                      variant="ghost"
                      size="xs"
                      @click="copyToClipboard(url.url)"
                    />
                    <UButton
                      icon="i-heroicons-arrow-top-right-on-square"
                      color="gray"
                      variant="ghost"
                      size="xs"
                      @click="openUrl(url.url)"
                    />
                    <UButton
                      icon="i-heroicons-magnifying-glass"
                      color="cyan"
                      variant="ghost"
                      size="xs"
                      @click="analyzeUrl(url.url)"
                    />
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </UCard>
    </template>
  </div>
</template>

<script setup>
const domain = ref('');
const isLoading = ref(false);
const error = ref(null);
const urls = ref([]);
const searchTerm = ref('');

const filteredUrls = computed(() => {
  if (!searchTerm.value) return urls.value;
  
  const term = searchTerm.value.toLowerCase();
  return urls.value.filter(url => url.url.toLowerCase().includes(term));
});

const findUrls = async () => {
  if (!domain.value.trim()) return;
  
  // Clean domain input
  let cleanDomain = domain.value.trim();
  cleanDomain = cleanDomain.replace(/^https?:\/\//, '');
  cleanDomain = cleanDomain.replace(/\/.*$/, '');
  
  isLoading.value = true;
  error.value = null;
  urls.value = [];
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Generate sample URLs
    const baseUrls = [
      '/',
      '/about',
      '/contact',
      '/login',
      '/register',
      '/admin',
      '/api',
      '/api/v1/users',
      '/api/v1/products',
      '/blog',
      '/products',
      '/services',
      '/cart',
      '/checkout',
      '/faq',
      '/terms',
      '/privacy',
      '/sitemap.xml',
      '/robots.txt',
      '/.git/config',
      '/wp-admin',
      '/wp-login.php',
      '/backup',
      '/old',
      '/dev',
      '/test',
      '/staging',
      '/beta',
      '/debug',
      '/phpinfo.php'
    ];
    
    // Create random dates for last seen
    const getRandomDate = () => {
      const start = new Date(2022, 0, 1);
      const end = new Date();
      const randomDate = new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
      return randomDate.toLocaleDateString();
    };
    
    // Generate full URLs
    urls.value = baseUrls.map(path => ({
      url: `https://${cleanDomain}${path}`,
      lastSeen: getRandomDate()
    }));
    
    // Add some random subpaths
    const subpaths = ['/index.php', '/index.html', '/default.aspx', '/main.js', '/styles.css', '/config.json'];
    const randomSubpaths = baseUrls
      .filter(() => Math.random() > 0.7)
      .map(path => ({
        url: `https://${cleanDomain}${path}${subpaths[Math.floor(Math.random() * subpaths.length)]}`,
        lastSeen: getRandomDate()
      }));
    
    urls.value = [...urls.value, ...randomSubpaths];
    
    // Sort by URL
    urls.value.sort((a, b) => a.url.localeCompare(b.url));
  } catch (e) {
    error.value = e.message || 'An unexpected error occurred';
  } finally {
    isLoading.value = false;
  }
};

const getUrlTypeIcon = (url) => {
  if (url.includes('/api/')) return 'i-heroicons-code-bracket';
  if (url.endsWith('.js')) return 'i-heroicons-code-bracket';
  if (url.endsWith('.css')) return 'i-heroicons-paint-brush';
  if (url.endsWith('.php')) return 'i-heroicons-document-text';
  if (url.endsWith('.xml')) return 'i-heroicons-document';
  if (url.endsWith('.txt')) return 'i-heroicons-document-text';
  if (url.includes('admin')) return 'i-heroicons-lock-closed';
  if (url.includes('login')) return 'i-heroicons-key';
  return 'i-heroicons-globe-alt';
};

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text);
    // Could show a toast notification here
  } catch (e) {
    console.error('Failed to copy to clipboard:', e);
  }
};

const openUrl = (url) => {
  window.open(url, '_blank');
};

const analyzeUrl = (url) => {
  navigateTo({
    path: '/',
    query: { url }
  });
};

const downloadResults = () => {
  // Create CSV content
  const csvContent = [
    'URL,Last Seen',
    ...filteredUrls.value.map(url => `${url.url},${url.lastSeen}`)
  ].join('\n');
  
  // Create download link
  const blob = new Blob([csvContent], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${domain.value}-urls.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
};
</script>
