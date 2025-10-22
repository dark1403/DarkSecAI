import apiClient from './apiClient';

// Define interfaces for chat data
interface ChatMessage {
  role: 'user' | 'model' | 'system';
  content: string;
  created_at?: string;
}

interface Conversation {
  id: string;
  title: string;
  messages: ChatMessage[];
  created_at: string;
}

interface SendMessageRequest {
  conversationId?: string;
  message: string;
}

interface SendMessageResponse {
  conversationId: string;
  message: string;
}

/**
 * Service for handling chat functionality
 */
const chatService = {
  /**
   * Get all conversations
   * @returns Promise with array of conversations
   */
  getConversations: async (): Promise<Conversation[]> => {
    try {
      const response = await apiClient.get('/conversations/');
      return response.data;
    } catch (error) {
      console.error('Error fetching conversations:', error);
      throw error;
    }
  },

  /**
   * Get a specific conversation
   * @param id Conversation ID
   * @returns Promise with conversation
   */
  getConversation: async (id: string): Promise<Conversation> => {
    try {
      const response = await apiClient.get(`/conversations/${id}/`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching conversation ${id}:`, error);
      throw error;
    }
  },

  /**
   * Get messages for a conversation
   * @param conversationId Conversation ID
   * @returns Promise with array of messages
   */
  getMessages: async (conversationId: string): Promise<ChatMessage[]> => {
    try {
      const response = await apiClient.get(`/chat/messages/?conversationId=${conversationId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching messages for conversation ${conversationId}:`, error);
      throw error;
    }
  },

  /**
   * Send a message to the AI
   * @param request Message request
   * @returns Promise with AI response
   */
  sendMessage: async (request: SendMessageRequest): Promise<SendMessageResponse> => {
    try {
      const response = await apiClient.post('/chat/messages/', request);
      return response.data;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  },

  /**
   * Create a new conversation
   * @param title Conversation title
   * @returns Promise with new conversation
   */
  createConversation: async (title: string): Promise<Conversation> => {
    try {
      const response = await apiClient.post('/conversations/', { title });
      return response.data;
    } catch (error) {
      console.error('Error creating conversation:', error);
      throw error;
    }
  },

  /**
   * Delete a conversation
   * @param id Conversation ID
   * @returns Promise with deletion status
   */
  deleteConversation: async (id: string): Promise<void> => {
    try {
      await apiClient.delete(`/conversations/${id}/`);
    } catch (error) {
      console.error(`Error deleting conversation ${id}:`, error);
      throw error;
    }
  }
};

export default chatService;