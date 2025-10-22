<script setup lang="ts">
import { useAuthStore } from '~/stores/auth';
import { useNavigation } from '~/composables/useNavigation';

const authStore = useAuthStore();
const route = useRoute();
const router = useRouter();
const { navigationLinks } = useNavigation();

const isSettingsOpen = ref(false);
const isUserDocsOpen = ref(false);
const isSidebarOpen = ref(true);

const openSettings = () => {
  isSettingsOpen.value = true;
};

const openUserDocs = () => {
  isUserDocsOpen.value = true;
};

const logout = () => {
  authStore.logout();
  router.push('/login');
};

const userInitials = computed(() => {
  if (!authStore.user?.username) return 'U';
  return authStore.user.username.substring(0, 2).toUpperCase();
});

const userMenuItems = [
  [
    {
      label: authStore.user?.username || 'User',
      slot: 'account',
      disabled: true
    }
  ],
  [
    {
      label: 'Settings',
      icon: 'i-heroicons-cog-6-tooth',
      click: openSettings
    },
    {
      label: 'Help',
      icon: 'i-heroicons-question-mark-circle',
      click: openUserDocs
    }
  ],
  [
    {
      label: 'Sign out',
      icon: 'i-heroicons-arrow-right-on-rectangle',
      click: logout
    }
  ]
];

// Check if we're on an auth page
const isAuthPage = computed(() => {
  const authPages = ['/login', '/register'];
  return authPages.includes(route.path);
});

// Check if we're logged in
const isLoggedIn = computed(() => authStore.isLoggedIn);

// Navigate to a page
const navigateTo = (path: string) => {
  router.push(path);
  // Close sidebar on mobile after navigation
  if (window.innerWidth < 1024) {
    isSidebarOpen.value = false;
  }
};

// Check if route is active
const isActiveRoute = (path: string) => {
  if (path === '/') return route.path === path;
  return route.path.startsWith(path);
};
</script>

<template>
  <!-- Auth Pages Layout -->
  <div v-if="isAuthPage" class="min-h-screen bg-gray-900">
    <slot />
  </div>

  <!-- Dashboard Layout for Authenticated Users -->
  <div v-else-if="isLoggedIn" class="min-h-screen bg-gray-900 flex">
    <!-- Sidebar -->
    <aside
      :class="[
        'fixed inset-y-0 left-0 z-50 flex flex-col bg-gray-800/50 border-r border-gray-700 transition-transform duration-300 backdrop-blur-sm',
        isSidebarOpen ? 'translate-x-0' : '-translate-x-full',
        'w-64 lg:translate-x-0'
      ]"
    >
      <!-- Sidebar Header -->
      <div class="flex items-center justify-between h-16 px-4 border-b border-gray-700">
        <NuxtLink to="/" class="flex items-center space-x-2">
          <span class="text-xl font-bold bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent">DarkSec-AI</span>
        </NuxtLink>
        <UButton
          icon="i-heroicons-x-mark"
          variant="ghost"
          color="gray"
          class="lg:hidden"
          @click="isSidebarOpen = false"
        />
      </div>

      <!-- Sidebar Navigation -->
      <div class="flex-1 overflow-y-auto px-3 py-4 space-y-1">
        <template v-for="item in navigationLinks" :key="item.label">
          <!-- Single Link Item -->
          <template v-if="!item.children">
            <UButton
              :to="item.to"
              :icon="item.icon"
              variant="ghost"
              color="gray"
              block
              :class="[
                'justify-start transition-colors',
                isActiveRoute(item.to) 
                  ? 'bg-primary/10 text-primary border-l-2 border-primary' 
                  : 'text-gray-300 hover:bg-gray-700/50 hover:text-white'
              ]"
              @click="navigateTo(item.to)"
            >
              {{ item.label }}
            </UButton>
          </template>

          <!-- Group with Children -->
          <template v-else>
            <div class="pt-4 pb-2 first:pt-0">
              <p class="px-3 text-xs font-semibold text-gray-400 uppercase tracking-wider">
                {{ item.label }}
              </p>
            </div>
            <UButton
              v-for="child in item.children"
              :key="child.to"
              :to="child.to"
              :icon="child.icon"
              variant="ghost"
              color="gray"
              block
              :class="[
                'justify-start transition-colors',
                isActiveRoute(child.to) 
                  ? 'bg-primary/10 text-primary border-l-2 border-primary' 
                  : 'text-gray-300 hover:bg-gray-700/50 hover:text-white'
              ]"
              @click="navigateTo(child.to)"
            >
              {{ child.label }}
            </UButton>
          </template>
        </template>
      </div>

      <!-- Sidebar Footer -->
      <div class="border-t border-gray-700 p-3">
        <UDropdown
          :items="userMenuItems"
          :popper="{ placement: 'top-start' }"
          :ui="{ width: 'w-full', item: { base: 'w-full' } }"
        >
          <template #default="{ open }">
            <UButton
              color="gray"
              variant="ghost"
              block
              :class="['transition-colors', open && 'bg-gray-700/50']"
            >
              <template #leading>
                <div class="h-8 w-8 rounded-full bg-gradient-to-r from-cyan-500 to-purple-500 flex items-center justify-center text-white font-medium text-sm ring-2 ring-gray-700">
                  {{ userInitials }}
                </div>
              </template>

              <div class="flex flex-col items-start flex-1 min-w-0 text-left">
                <span class="text-sm font-medium truncate w-full text-white">{{ authStore.user?.username }}</span>
                <span class="text-xs text-gray-400 truncate w-full">{{ authStore.user?.email }}</span>
              </div>

              <template #trailing>
                <UIcon
                  name="i-heroicons-ellipsis-vertical"
                  class="h-5 w-5 text-gray-400"
                />
              </template>
            </UButton>
          </template>

          <template #account>
            <div class="text-left px-2 py-1.5">
              <p class="text-sm font-medium text-gray-900 dark:text-white truncate">
                {{ authStore.user?.username }}
              </p>
              <p class="text-sm text-gray-500 dark:text-gray-400 truncate">
                {{ authStore.user?.email }}
              </p>
            </div>
          </template>
        </UDropdown>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col lg:ml-64">
      <!-- Top Navbar -->
      <header class="sticky top-0 z-40 bg-gray-800/95 backdrop-blur-sm border-b border-gray-700">
        <div class="flex items-center justify-between h-16 px-4">
          <div class="flex items-center space-x-3">
            <UButton
              icon="i-heroicons-bars-3"
              variant="ghost"
              color="gray"
              class="lg:hidden"
              @click="isSidebarOpen = true"
            />
            <h1 class="text-lg font-semibold bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent lg:hidden">DarkSec-AI</h1>
          </div>

          <div class="flex items-center space-x-2">
            <UTooltip text="WebSec Agent">
              <UButton
                icon="i-heroicons-chat-bubble-left-right"
                variant="ghost"
                color="gray"
                to="/websec-agent"
                class="hover:bg-primary/10 hover:text-primary transition-colors"
              />
            </UTooltip>

            <UTooltip text="Developer Info">
              <UButton
                icon="i-heroicons-users"
                variant="ghost"
                color="gray"
                to="/developer-showcase"
                class="hover:bg-primary/10 hover:text-primary transition-colors"
              />
            </UTooltip>

            <UTooltip text="Help">
              <UButton
                icon="i-heroicons-question-mark-circle"
                variant="ghost"
                color="gray"
                @click="openUserDocs"
                class="hover:bg-primary/10 hover:text-primary transition-colors"
              />
            </UTooltip>
          </div>
        </div>
      </header>

      <!-- Page Content -->
      <main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">
        <div class="max-w-7xl mx-auto">
          <slot />
        </div>
      </main>
    </div>

    <!-- Mobile Sidebar Overlay -->
    <div
      v-if="isSidebarOpen"
      class="fixed inset-0 bg-gray-900/50 backdrop-blur-sm z-40 lg:hidden transition-opacity"
      @click="isSidebarOpen = false"
    />

    <!-- Modals -->
    <UModal v-model="isSettingsOpen">
      <SettingsModal @close="isSettingsOpen = false" />
    </UModal>

    <UModal v-model="isUserDocsOpen">
      <UserDocumentationModal @close="isUserDocsOpen = false" />
    </UModal>
  </div>

  <!-- Fallback for non-authenticated users -->
  <div v-else class="min-h-screen bg-gray-900">
    <slot />
  </div>
</template>