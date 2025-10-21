/**
 * API Service Layer for AgenticKanban
 * Handles HTTP requests to the FastAPI backend
 */

// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const API_VERSION = 'v1';
const API_PREFIX = `${API_BASE_URL}/api/${API_VERSION}`;

// Request timeout in milliseconds
const REQUEST_TIMEOUT = 30000;

// API Error Classes
export class APIError extends Error {
  constructor(message, status, details = null) {
    super(message);
    this.name = 'APIError';
    this.status = status;
    this.details = details;
  }
}

export class NetworkError extends Error {
  constructor(message) {
    super(message);
    this.name = 'NetworkError';
  }
}

// HTTP Client with error handling and retries
class HTTPClient {
  constructor() {
    this.defaultHeaders = {
      'Content-Type': 'application/json',
    };
  }

  async request(url, options = {}) {
    const config = {
      method: 'GET',
      headers: { ...this.defaultHeaders, ...options.headers },
      ...options,
    };

    // Add timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT);
    config.signal = controller.signal;

    try {
      const response = await fetch(`${API_PREFIX}${url}`, config);
      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new APIError(
          errorData.error || `HTTP ${response.status}: ${response.statusText}`,
          response.status,
          errorData.details
        );
      }

      // Handle 204 No Content responses
      if (response.status === 204) {
        return null;
      }

      return await response.json();
    } catch (error) {
      clearTimeout(timeoutId);

      if (error.name === 'AbortError') {
        throw new NetworkError('Request timeout');
      }

      if (error instanceof APIError) {
        throw error;
      }

      if (error.name === 'TypeError' || !navigator.onLine) {
        throw new NetworkError('Network connection error');
      }

      throw new APIError('Unexpected error occurred', 0, error.message);
    }
  }

  async get(url, params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const fullUrl = queryString ? `${url}?${queryString}` : url;
    return this.request(fullUrl);
  }

  async post(url, data = {}) {
    return this.request(url, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async put(url, data = {}) {
    return this.request(url, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async delete(url) {
    return this.request(url, {
      method: 'DELETE',
    });
  }
}

// Create HTTP client instance
const httpClient = new HTTPClient();

// Workflow API Functions
export const workflowAPI = {
  /**
   * Create a new workflow task
   * @param {Object} taskData - Task creation data
   * @param {string} taskData.title - Task title
   * @param {string} taskData.description - Task description
   * @param {string} taskData.task_type - Task type (feature, bug, etc.)
   * @param {string[]} taskData.stages - Workflow stages
   * @returns {Promise<Object>} Created task data
   */
  async create(taskData) {
    console.log('API: Creating workflow task', taskData);
    try {
      const response = await httpClient.post('/workflows/create', taskData);
      console.log('API: Workflow task created successfully', response);
      return response;
    } catch (error) {
      console.error('API: Failed to create workflow task', error);
      throw error;
    }
  },

  /**
   * Get workflow task by ADW ID
   * @param {string} adwId - ADW identifier
   * @returns {Promise<Object>} Task data
   */
  async get(adwId) {
    console.log('API: Getting workflow task', adwId);
    try {
      const response = await httpClient.get(`/workflows/${adwId}`);
      console.log('API: Workflow task retrieved', response);
      return response;
    } catch (error) {
      console.error('API: Failed to get workflow task', error);
      throw error;
    }
  },

  /**
   * Update workflow task status
   * @param {string} adwId - ADW identifier
   * @param {Object} updateData - Update data
   * @returns {Promise<Object>} Updated task data
   */
  async updateStatus(adwId, updateData) {
    console.log('API: Updating workflow status', adwId, updateData);
    try {
      const response = await httpClient.put(`/workflows/${adwId}/status`, updateData);
      console.log('API: Workflow status updated', response);
      return response;
    } catch (error) {
      console.error('API: Failed to update workflow status', error);
      throw error;
    }
  },

  /**
   * Cancel/delete workflow task
   * @param {string} adwId - ADW identifier
   * @returns {Promise<void>}
   */
  async cancel(adwId) {
    console.log('API: Cancelling workflow task', adwId);
    try {
      await httpClient.delete(`/workflows/${adwId}`);
      console.log('API: Workflow task cancelled');
    } catch (error) {
      console.error('API: Failed to cancel workflow task', error);
      throw error;
    }
  },

  /**
   * List workflow tasks with pagination
   * @param {Object} params - Query parameters
   * @param {number} params.page - Page number
   * @param {number} params.per_page - Items per page
   * @param {string} params.status - Filter by status
   * @param {string} params.task_type - Filter by task type
   * @returns {Promise<Object>} Paginated task list
   */
  async list(params = {}) {
    console.log('API: Listing workflow tasks', params);
    try {
      const response = await httpClient.get('/workflows', params);
      console.log('API: Workflow tasks retrieved', response);
      return response;
    } catch (error) {
      console.error('API: Failed to list workflow tasks', error);
      throw error;
    }
  },
};

// Health Check API
export const healthAPI = {
  /**
   * Check API server health
   * @returns {Promise<Object>} Health status
   */
  async check() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      if (!response.ok) {
        throw new APIError('Health check failed', response.status);
      }
      return await response.json();
    } catch (error) {
      console.error('API: Health check failed', error);
      throw error;
    }
  },
};

// Utility functions
export const utils = {
  /**
   * Check if API is available
   * @returns {Promise<boolean>} API availability
   */
  async isAPIAvailable() {
    try {
      await healthAPI.check();
      return true;
    } catch (error) {
      return false;
    }
  },

  /**
   * Get API base URL
   * @returns {string} API base URL
   */
  getAPIBaseURL() {
    return API_BASE_URL;
  },

  /**
   * Format error for display
   * @param {Error} error - Error object
   * @returns {string} Formatted error message
   */
  formatError(error) {
    if (error instanceof APIError) {
      return `API Error (${error.status}): ${error.message}`;
    }
    if (error instanceof NetworkError) {
      return `Network Error: ${error.message}`;
    }
    return `Error: ${error.message}`;
  },
};

// Export default API object
export default {
  workflow: workflowAPI,
  health: healthAPI,
  utils,
  errors: {
    APIError,
    NetworkError,
  },
};