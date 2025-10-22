import { useAuthStore } from '~/stores/auth';

export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore();
  
  // Initialize auth store
  authStore.initialize();
  
  // If user is not logged in and trying to access a protected route
  if (!authStore.isLoggedIn && to.path !== '/login' && to.path !== '/register') {
    return navigateTo('/login');
  }
  
  // If user is logged in and trying to access login or register page
  if (authStore.isLoggedIn && (to.path === '/login' || to.path === '/register')) {
    return navigateTo('/');
  }
});
