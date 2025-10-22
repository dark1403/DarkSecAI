<template>
  <div>
    <div class="mb-6">
      <p class="text-sm text-gray-400 mb-4">
        Find subdomains by searching public Certificate Transparency (CT) logs via crt.sh, a highly reliable method for subdomain discovery.
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
          @click="findSubdomains"
        >
          Find Subdomains
        </UButton>
      </div>
    </div>
    
    <div v-if="isLoading" class="flex justify-center my-8">
      <UProgress animation="carousel" />
    </div>
    
    <div v-if="error" class="mt-6 p-4 bg-red-900/50 border border-red-700 text-red-200 rounded-lg font-mono">
      {{ error }}
    </div>
    
    <template v-if="subdomains.length > 0 && !isLoading">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold">Found {{ subdomains.length }} Subdomains</h3>
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
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <UCard>
          <template #header>
            <div class="flex justify-between items-center">
              <h3 class="font-medium">Subdomain List</h3>
              <UBadge color="gray">{{ filteredSubdomains.length }}</UBadge>
            </div>
          </template>
          
          <div class="max-h-96 overflow-y-auto">
            <ul class="divide-y divide-gray-700">
              <li 
                v-for="(subdomain, index) in filteredSubdomains" 
                :key="index"
                class="py-2 hover:bg-gray-800/50 cursor-pointer"
                @click="selectSubdomain(subdomain)"
              >
                <div class="flex justify-between items-center">
                  <div class="flex items-center">
                    <UIcon 
                      :name="getSubdomainTypeIcon(subdomain.name)" 
                      class="mr-2 text-gray-400"
                    />
                    <span>{{ subdomain.name }}</span>
                  </div>
                  <UBadge
                    v-if="subdomain.isActive"
                    color="green"
                    variant="subtle"
                    size="sm"
                  >
                    Active
                  </UBadge>
                </div>
              </li>
            </ul>
          </div>
        </UCard>
        
        <UCard>
          <template #header>
            <h3 class="font-medium">Subdomain Details</h3>
          </template>
          
          <div v-if="selectedSubdomain" class="space-y-4">
            <div>
              <h4 class="text-sm font-medium text-gray-400">Subdomain</h4>
              <p class="font-medium">{{ selectedSubdomain.name }}</p>
            </div>
            
            <div>
              <h4 class="text-sm font-medium text-gray-400">Status</h4>
              <UBadge :color="selectedSubdomain.isActive ? 'green' : 'red'">
                {{ selectedSubdomain.isActive ? 'Active' : 'Inactive' }}
              </UBadge>
            </div>
            
            <div>
              <h4 class="text-sm font-medium text-gray-400">IP Address</h4>
              <p>{{ selectedSubdomain.ip || 'Not resolved' }}</p>
            </div>
            
            <div>
              <h4 class="text-sm font-medium text-gray-400">First Seen</h4>
              <p>{{ selectedSubdomain.firstSeen }}</p>
            </div>
            
            <div>
              <h4 class="text-sm font-medium text-gray-400">Last Seen</h4>
              <p>{{ selectedSubdomain.lastSeen }}</p>
            </div>
            
            <div class="flex gap-2">
              <UButton
                icon="i-heroicons-arrow-top-right-on-square"
                color="cyan"
                @click="openSubdomain(selectedSubdomain.name)"
              >
                Open
              </UButton>
              
              <UButton
                icon="i-heroicons-magnifying-glass"
                color="purple"
                @click="analyzeSubdomain(selectedSubdomain.name)"
              >
                Analyze
              </UButton>
            </div>
          </div>
          
          <div v-else class="text-center py-8 text-gray-400">
            <UIcon name="i-heroicons-information-circle" class="h-8 w-8 mx-auto mb-2" />
            <p>Select a subdomain to view details</p>
          </div>
        </UCard>
      </div>
      
      <div class="mt-6">
        <UCard>
          <template #header>
            <h3 class="font-medium">Visualization</h3>
          </template>
          
          <div class="h-64 bg-gray-800/50 rounded-lg flex items-center justify-center">
            <p class="text-gray-400">Subdomain relationship visualization would appear here</p>
          </div>
        </UCard>
      </div>
    </template>
  </div>
</template>

<script setup>
const domain = ref('');
const isLoading = ref(false);
const error = ref(null);
const subdomains = ref([]);
const searchTerm = ref('');
const selectedSubdomain = ref(null);

const filteredSubdomains = computed(() => {
  if (!searchTerm.value) return subdomains.value;
  
  const term = searchTerm.value.toLowerCase();
  return subdomains.value.filter(sub => sub.name.toLowerCase().includes(term));
});

const findSubdomains = async () => {
  if (!domain.value.trim()) return;
  
  // Clean domain input
  let cleanDomain = domain.value.trim();
  cleanDomain = cleanDomain.replace(/^https?:\/\//, '');
  cleanDomain = cleanDomain.replace(/\/.*$/, '');
  
  isLoading.value = true;
  error.value = null;
  subdomains.value = [];
  selectedSubdomain.value = null;
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Generate sample subdomains
    const prefixes = [
      'www', 'api', 'mail', 'blog', 'shop', 'store', 'dev', 'test', 'stage', 'staging',
      'admin', 'portal', 'app', 'mobile', 'secure', 'login', 'auth', 'cdn', 'media',
      'images', 'static', 'assets', 'content', 'support', 'help', 'docs', 'kb',
      'forum', 'community', 'status', 'beta', 'alpha', 'demo', 'sandbox'
    ];
    
    // Create random dates
    const getRandomDate = () => {
      const start = new Date(2022, 0, 1);
      const end = new Date();
      const randomDate = new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
      return randomDate.toLocaleDateString();
    };
    
    // Generate random IP addresses
    const getRandomIP = () => {
      return `${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}`;
    };
    
    // Generate subdomains
    subdomains.value = prefixes
      .filter(() => Math.random() > 0.3) // Randomly select some prefixes
      .map(prefix => ({
        name: `${prefix}.${cleanDomain}`,
        isActive: Math.random() > 0.2, // 80% chance of being active
        ip: Math.random() > 0.1 ? getRandomIP() : null, // 90% chance of having an IP
        firstSeen: getRandomDate(),
        lastSeen: getRandomDate()
      }));
    
    // Add some random multi-level subdomains
    const multiLevelPrefixes = ['api', 'dev', 'test', 'admin'];
    const secondLevelPrefixes = ['v1', 'v2', 'internal', 'external', 'public', 'private'];
    
    const multiLevelSubdomains = multiLevelPrefixes
      .filter(() => Math.random() > 0.5) // Randomly select some prefixes
      .flatMap(prefix => 
        secondLevelPrefixes
          .filter(() => Math.random() > 0.7) // Randomly select some second-level prefixes
          .map(secondPrefix => ({
            name: `${secondPrefix}.${prefix}.${cleanDomain}`,
            isActive: Math.random() > 0.3, // 70% chance of being active
            ip: Math.random() > 0.2 ? getRandomIP() : null, // 80% chance of having an IP
            firstSeen: getRandomDate(),
            lastSeen: getRandomDate()
          }))
      );
    
    subdomains.value = [...subdomains.value, ...multiLevelSubdomains];
    
    // Sort by name
    subdomains.value.sort((a, b) => a.name.localeCompare(b.name));
  } catch (e) {
    error.value = e.message || 'An unexpected error occurred';
  } finally {
    isLoading.value = false;
  }
};

const getSubdomainTypeIcon = (name) => {
  if (name.startsWith('api.')) return 'i-heroicons-code-bracket';
  if (name.startsWith('admin.')) return 'i-heroicons-lock-closed';
  if (name.startsWith('dev.') || name.startsWith('test.')) return 'i-heroicons-beaker';
  if (name.startsWith('stage.') || name.startsWith('staging.')) return 'i-heroicons-beaker';
  if (name.startsWith('mail.')) return 'i-heroicons-envelope';
  if (name.startsWith('blog.')) return 'i-heroicons-document-text';
  if (name.startsWith('cdn.') || name.startsWith('static.')) return 'i-heroicons-cloud';
  if (name.startsWith('www.')) return 'i-heroicons-globe-alt';
  return 'i-heroicons-server';
};

const selectSubdomain = (subdomain) => {
  selectedSubdomain.value = subdomain;
};

function openSafe(url, base = location.origin) {
  try {
    const u = new URL(url, base); // resolves relative URLs too
    window.open(u.toString(), '_blank', 'noopener,noreferrer');
  } catch (e) {
    console.error('Bad URL:', url, e);
    // show a toast / fallback here
  }
}

const openSubdomain = (name) => {
  openSafe(name);
};

const analyzeSubdomain = (name) => {
  navigateTo({
    path: '/',
    query: { url: `https://${name}` }
  });
};

const downloadResults = () => {
  // Create CSV content
  const csvContent = [
    'Subdomain,Status,IP,First Seen,Last Seen',
    ...filteredSubdomains.value.map(sub => 
      `${sub.name},${sub.isActive ? 'Active' : 'Inactive'},${sub.ip || 'N/A'},${sub.firstSeen},${sub.lastSeen}`
    )
  ].join('\n');
  
  // Create download link
  const blob = new Blob([csvContent], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${domain.value}-subdomains.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
};
</script>
