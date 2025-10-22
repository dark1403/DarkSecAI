import { defineStore } from 'pinia';
import { authService } from '../services/api';

interface User {
  id: string;
  username: string;
  email: string;
  role: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    token: null,
    isAuthenticated: false,
    isLoading: false,
    error: null
  }),
  
  actions: {
    initialize() {
      // Check if user is already logged in
      if (typeof window !== 'undefined') {
        const token = localStorage.getItem('auth_token');
        const user = localStorage.getItem('auth_user');
        
        if (token && user) {
          this.token = token;
          this.user = JSON.parse(user);
          this.isAuthenticated = true;
        }
      }
    },
    
    async login(username: string, password: string) {
      this.isLoading = true;
      this.error = null;
      
      try {
        // Call the real API
        const response = await authService.login({ username, password });
        
        // Save to state
        this.user = response.user;
        this.token = response.token;
        this.isAuthenticated = true;
        
        return true;
      } catch (error: any) {
        // Handle API errors
        if (error.response && error.response.data && error.response.data.error) {
          this.error = error.response.data.error;
        } else {
          this.error = error.message || 'Failed to login';
        }
        return false;
      } finally {
        this.isLoading = false;
      }
    },
    
    async register(username: string, email: string, password: string) {
      this.isLoading = true;
      this.error = null;
      
      try {
        // Call the real API
        const response = await authService.register({ username, email, password });
        
        // Save to state
        this.user = response.user;
        this.token = response.token;
        this.isAuthenticated = true;
        
        return true;
      } catch (error: any) {
        // Handle API errors
        if (error.response && error.response.data && error.response.data.error) {
          this.error = error.response.data.error;
        } else {
          this.error = error.message || 'Failed to register';
        }
        return false;
      } finally {
        this.isLoading = false;
      }
    },
    
    logout() {
      // Call the auth service to logout
      authService.logout();
      
      // Clear state
      this.user = null;
      this.token = null;
      this.isAuthenticated = false;
    },
    
    async verifyToken() {
      if (!this.token) return false;
      
      try {
        return await authService.verifyToken();
      } catch (error) {
        this.logout();
        return false;
      }
    }
  },
  
  getters: {
    isLoggedIn(): boolean {
      return this.isAuthenticated;
    },
    
    currentUser(): User | null {
      return this.user;
    },
    
    userRole(): string | null {
      return this.user?.role || null;
    }
  }
});
