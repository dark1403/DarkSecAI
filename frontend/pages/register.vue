<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-gray-900 to-gray-800 py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
    <!-- Animated background -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl animate-pulse"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-pink-500/10 rounded-full blur-3xl animate-pulse" style="animation-delay: 1s"></div>
    </div>
    
    <div class="max-w-md w-full space-y-8 relative z-10">
      <div class="text-center">
        <div class="inline-block p-3 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-2xl mb-4 backdrop-blur-sm border border-purple-500/20">
          <UIcon name="i-heroicons-user-plus" class="h-12 w-12 text-purple-400" />
        </div>
        <h1 class="text-4xl font-extrabold bg-gradient-to-r from-purple-400 via-pink-400 to-red-400 bg-clip-text text-transparent">
          DarkSec-AI
        </h1>
        <h2 class="mt-6 text-2xl font-bold text-white">Create a new account</h2>
        <p class="mt-2 text-sm text-gray-400">
          Or
          <NuxtLink to="/login" class="font-semibold text-purple-400 hover:text-purple-300 transition-colors">
            sign in to your account
          </NuxtLink>
        </p>
      </div>
      
      <UCard class="mt-8 bg-gray-800/50 border-gray-700/50 backdrop-blur-sm shadow-2xl">
        <UForm :state="form" class="space-y-6" @submit="handleRegister">
          <UFormGroup label="Username" name="username">
            <UInput
              v-model="form.username"
              placeholder="Choose a username"
              autocomplete="username"
              size="lg"
              icon="i-heroicons-user"
              :ui="{ 
                base: 'bg-gray-700/50 border-gray-600 focus:border-purple-500 focus:ring-purple-500/50 backdrop-blur-sm',
                icon: { leading: { wrapper: 'text-gray-400' } }
              }"
              required
            />
          </UFormGroup>
          
          <UFormGroup label="Email" name="email">
            <UInput
              v-model="form.email"
              type="email"
              placeholder="Enter your email"
              autocomplete="email"
              size="lg"
              icon="i-heroicons-envelope"
              :ui="{ 
                base: 'bg-gray-700/50 border-gray-600 focus:border-purple-500 focus:ring-purple-500/50 backdrop-blur-sm',
                icon: { leading: { wrapper: 'text-gray-400' } }
              }"
              required
            />
          </UFormGroup>
          
          <UFormGroup label="Password" name="password">
            <UInput
              v-model="form.password"
              type="password"
              placeholder="Create a password"
              autocomplete="new-password"
              size="lg"
              icon="i-heroicons-lock-closed"
              :ui="{ 
                base: 'bg-gray-700/50 border-gray-600 focus:border-purple-500 focus:ring-purple-500/50 backdrop-blur-sm',
                icon: { leading: { wrapper: 'text-gray-400' } }
              }"
              required
            />
          </UFormGroup>
          
          <UFormGroup label="Confirm Password" name="confirmPassword">
            <UInput
              v-model="form.confirmPassword"
              type="password"
              placeholder="Confirm your password"
              autocomplete="new-password"
              size="lg"
              icon="i-heroicons-lock-closed"
              :ui="{ 
                base: 'bg-gray-700/50 border-gray-600 focus:border-purple-500 focus:ring-purple-500/50 backdrop-blur-sm',
                icon: { leading: { wrapper: 'text-gray-400' } }
              }"
              required
            />
          </UFormGroup>
          
          <div>
            <UCheckbox
              v-model="form.terms"
              label="I agree to the Terms of Service and Privacy Policy"
              name="terms"
              required
            />
          </div>
          
          <div v-if="authStore.error" class="p-4 bg-red-900/30 border border-red-700/50 rounded-lg text-red-200 text-sm backdrop-blur-sm flex items-start gap-2">
            <UIcon name="i-heroicons-exclamation-triangle" class="h-5 w-5 flex-shrink-0 mt-0.5" />
            <span>{{ authStore.error }}</span>
          </div>
          
          <div v-if="formError" class="p-4 bg-red-900/30 border border-red-700/50 rounded-lg text-red-200 text-sm backdrop-blur-sm flex items-start gap-2">
            <UIcon name="i-heroicons-exclamation-triangle" class="h-5 w-5 flex-shrink-0 mt-0.5" />
            <span>{{ formError }}</span>
          </div>
          
          <div>
            <UButton
              type="submit"
              block
              size="xl"
              color="purple"
              :loading="authStore.isLoading"
              class="shadow-lg shadow-purple-500/25 hover:shadow-xl hover:shadow-purple-500/40 transition-all hover:scale-[1.02]"
            >
              <span class="font-semibold">Create Account</span>
            </UButton>
          </div>
        </UForm>
      </UCard>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '~/stores/auth';

const router = useRouter();
const authStore = useAuthStore();
const formError = ref('');

const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  terms: false
});

// Redirect if already logged in
onMounted(() => {
  authStore.initialize();
  if (authStore.isLoggedIn) {
    router.push('/');
  }
});

const handleRegister = async () => {
  formError.value = '';
  
  // Validate form
  if (form.password !== form.confirmPassword) {
    formError.value = 'Passwords do not match';
    return;
  }
  
  if (!form.terms) {
    formError.value = 'You must agree to the Terms of Service';
    return;
  }
  
  const success = await authStore.register(form.username, form.email, form.password);
  if (success) {
    router.push('/');
  }
};
</script>