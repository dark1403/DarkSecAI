import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';

// Define the base API configuration
const apiConfig: AxiosRequestConfig = {
  baseURL: 'https://darksecai.onrender.com/api', // Assuming the API is served at /api
  // timeout: 120000, // 120 seconds (2 minutes) timeout for AI operations
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
};

// Create the Axios instance
const apiClient: AxiosInstance = axios.create(apiConfig);

// Request interceptor for adding auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers['Authorization'] = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling errors
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error: AxiosError) => {
    // Handle different error statuses
    if (error.response) {
      const { status } = error.response;
      
      // Handle authentication errors
      if (status === 401) {
        // Clear local storage and redirect to login if unauthorized
        localStorage.removeItem('auth_token');
        localStorage.removeItem('auth_user');
        window.location.href = '/login';
      }
      
      // Handle forbidden errors
      if (status === 403) {
        console.error('Permission denied');
      }
      
      // Handle not found errors
      if (status === 404) {
        console.error('Resource not found');
      }
      
      // Handle server errors
      if (status >= 500) {
        console.error('Server error');
      }
    } else if (error.request) {
      // The request was made but no response was received
      console.error('Network error - no response received');
    } else {
      // Something happened in setting up the request
      console.error('Error', error.message);
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;