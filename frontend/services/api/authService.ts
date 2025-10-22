import apiClient from './apiClient';

// Define interfaces for auth data
interface LoginCredentials {
  username: string;
  password: string;
}

interface RegisterCredentials {
  username: string;
  email: string;
  password: string;
}

interface User {
  id: string;
  username: string;
  email: string;
  role: string;
}

interface AuthResponse {
  token: string;
  user: User;
}

/**
 * Authentication service for handling user authentication
 */
const authService = {
  /**
   * Login a user
   * @param credentials User login credentials
   * @returns Promise with auth response
   */
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    try {
      const response = await apiClient.post('/auth/login/', credentials);
      
      // Store auth data in localStorage
      if (response.data.token) {
        localStorage.setItem('auth_token', response.data.token);
        localStorage.setItem('auth_user', JSON.stringify(response.data.user));
      }
      
      return response.data;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  },
  
  /**
   * Register a new user
   * @param credentials User registration credentials
   * @returns Promise with auth response
   */
  register: async (credentials: RegisterCredentials): Promise<AuthResponse> => {
    try {
      const response = await apiClient.post('/auth/register/', credentials);
      
      // Store auth data in localStorage
      if (response.data.token) {
        localStorage.setItem('auth_token', response.data.token);
        localStorage.setItem('auth_user', JSON.stringify(response.data.user));
      }
      
      return response.data;
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  },
  
  /**
   * Logout the current user
   */
  logout: (): void => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_user');
  },
  
  /**
   * Check if user is authenticated
   * @returns Boolean indicating if user is authenticated
   */
  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('auth_token');
  },
  
  /**
   * Get the current authenticated user
   * @returns User object or null if not authenticated
   */
  getCurrentUser: (): User | null => {
    const userJson = localStorage.getItem('auth_user');
    return userJson ? JSON.parse(userJson) : null;
  },
  
  /**
   * Verify the current token is still valid
   * @returns Promise with boolean indicating if token is valid
   */
  verifyToken: async (): Promise<boolean> => {
    try {
      const response = await apiClient.post('/auth/verify-token/');
      return response.status === 200;
    } catch (error) {
      console.error('Token verification error:', error);
      return false;
    }
  }
};

export default authService;