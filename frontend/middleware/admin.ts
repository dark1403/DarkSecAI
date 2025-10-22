import { useAuthStore } from '~/stores/auth';

export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore();

  // Ensure auth state is initialized
  authStore.initialize();

  // Only allow users with admin role
  if (authStore.userRole !== 'admin') {
    return navigateTo('/');
  }
});

