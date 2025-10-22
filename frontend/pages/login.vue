<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-gray-900 to-gray-800 py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
    <!-- Animated background -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-cyan-500/10 rounded-full blur-3xl animate-pulse"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl animate-pulse" style="animation-delay: 1s"></div>
    </div>
    
    <div class="max-w-md w-full space-y-8 relative z-10">
      <div class="text-center">
        <div class="inline-block p-3 bg-gradient-to-br from-cyan-500/20 to-purple-500/20 rounded-2xl mb-4 backdrop-blur-sm border border-cyan-500/20">
          <UIcon name="i-heroicons-shield-check" class="h-12 w-12 text-cyan-400" />
        </div>
        <h1 class="text-4xl font-extrabold bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
          DarkSec-AI
        </h1>
        <h2 class="mt-6 text-2xl font-bold text-white">Sign in to your account</h2>
        <p class="mt-2 text-sm text-gray-400">
          Or
          <NuxtLink to="/register" class="font-semibold text-cyan-400 hover:text-cyan-300 transition-colors">
            create a new account
          </NuxtLink>
        </p>
      </div>
      
      <UCard class="mt-8 bg-gray-800/50 border-gray-700/50 backdrop-blur-sm shadow-2xl">
        <UForm :state="form" class="space-y-6" @submit="handleLogin">
          <UFormGroup label="Username" name="username">
            <UInput
              v-model="form.username"
              placeholder="Enter your username"
              autocomplete="username"
              size="lg"
              icon="i-heroicons-user"
              :ui="{ 
                base: 'bg-gray-700/50 border-gray-600 focus:border-cyan-500 focus:ring-cyan-500/50 backdrop-blur-sm',
                icon: { leading: { wrapper: 'text-gray-400' } }
              }"
              required
            />
          </UFormGroup>
          
          <UFormGroup label="Password" name="password">
            <UInput
              v-model="form.password"
              type="password"
              placeholder="Enter your password"
              autocomplete="current-password"
              size="lg"
              icon="i-heroicons-lock-closed"
              :ui="{ 
                base: 'bg-gray-700/50 border-gray-600 focus:border-cyan-500 focus:ring-cyan-500/50 backdrop-blur-sm',
                icon: { leading: { wrapper: 'text-gray-400' } }
              }"
              required
            />
          </UFormGroup>
          
          <div class="flex items-center justify-between">
            <UCheckbox
              v-model="form.remember"
              label="Remember me"
              name="remember"
            />
            
            <NuxtLink to="#" class="text-sm font-medium text-cyan-400 hover:text-cyan-300 transition-colors">
              Forgot your password?
            </NuxtLink>
          </div>
          
          <div v-if="authStore.error" class="p-4 bg-red-900/30 border border-red-700/50 rounded-lg text-red-200 text-sm backdrop-blur-sm flex items-start gap-2">
            <UIcon name="i-heroicons-exclamation-triangle" class="h-5 w-5 flex-shrink-0 mt-0.5" />
            <span>{{ authStore.error }}</span>
          </div>
          
          <div>
            <UButton
              type="submit"
              block
              size="xl"
              color="cyan"
              :loading="authStore.isLoading"
              class="shadow-lg shadow-cyan-500/25 hover:shadow-xl hover:shadow-cyan-500/40 transition-all hover:scale-[1.02]"
            >
              <span class="font-semibold">Sign in</span>
            </UButton>
          </div>
        </UForm>
      </UCard>
      
      <div class="mt-6">
        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-700"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-3 bg-gray-900 text-gray-400 font-medium">Note</span>
          </div>
        </div>
        
        <div class="mt-6 grid grid-cols-2 gap-3">
          <div class="col-span-2">
            <div class="p-3 bg-yellow-900/30 border border-yellow-700/50 rounded-lg text-yellow-200 text-xs text-center backdrop-blur-sm">
              <UIcon name="i-heroicons-exclamation-circle" class="inline-block h-4 w-4 mr-1 align-text-bottom" />
              You are solely responsible for any misuse of this application. The developer is not responsible for your actions.
            </div>
          </div>
          <!-- <UButton
            color="gray"
            variant="soft"
            size="lg"
            class="hover:scale-105 transition-transform"
            @click="fillTestUser('user')"
          >
            <UIcon name="i-heroicons-user" class="h-4 w-4 mr-2" />
            Test User
          </UButton>
          <UButton
            color="gray"
            variant="soft"
            size="lg"
            class="hover:scale-105 transition-transform"
            @click="fillTestUser('admin')"
          >
            <UIcon name="i-heroicons-user-circle" class="h-4 w-4 mr-2" />
            Admin User
          </UButton> -->
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '~/stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const form = reactive({
  username: '',
  password: '',
  remember: false
});

// Redirect if already logged in
onMounted(() => {
  authStore.initialize();
  if (authStore.isLoggedIn) {
    router.push('/');
  }
});

const handleLogin = async () => {
  const success = await authStore.login(form.username, form.password);
  if (success) {
    router.push('/');
  }
};

const fillTestUser = (type) => {
  if (type === 'user') {
    form.username = 'testuser';
    form.password = 'testpassword';
  } else {
    form.username = 'admin';
    form.password = 'adminpassword';
  }
};
</script>