/**
 * WebSocket Service for real-time updates
 * Handles WebSocket connections and message broadcasting
 */

// WebSocket Configuration
const WS_BASE_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8000';
const RECONNECT_INTERVAL = 5000; // 5 seconds
const MAX_RECONNECT_ATTEMPTS = 10;
const HEARTBEAT_INTERVAL = 30000; // 30 seconds

// WebSocket Connection States
export const CONNECTION_STATES = {
  CONNECTING: 'connecting',
  CONNECTED: 'connected',
  DISCONNECTED: 'disconnected',
  RECONNECTING: 'reconnecting',
  FAILED: 'failed',
};

// Message Types
export const MESSAGE_TYPES = {
  TASK_CREATED: 'task_created',
  STATUS_UPDATE: 'status_update',
  STAGE_UPDATE: 'stage_update',
  PROGRESS_UPDATE: 'progress_update',
  TASK_CANCELLED: 'task_cancelled',
  CONNECTION_ESTABLISHED: 'connection_established',
  GLOBAL_CONNECTION_ESTABLISHED: 'global_connection_established',
  PING: 'ping',
  PONG: 'pong',
};

/**
 * WebSocket Connection Manager
 */
class WebSocketConnection {
  constructor(url, options = {}) {
    this.url = url;
    this.options = {
      autoReconnect: true,
      maxReconnectAttempts: MAX_RECONNECT_ATTEMPTS,
      reconnectInterval: RECONNECT_INTERVAL,
      heartbeatInterval: HEARTBEAT_INTERVAL,
      ...options,
    };

    this.ws = null;
    this.state = CONNECTION_STATES.DISCONNECTED;
    this.reconnectAttempts = 0;
    this.reconnectTimeout = null;
    this.heartbeatInterval = null;
    this.lastHeartbeat = null;

    // Event listeners
    this.listeners = {
      message: new Set(),
      stateChange: new Set(),
      error: new Set(),
    };

    this.connect();
  }

  /**
   * Establish WebSocket connection
   */
  connect() {
    if (this.state === CONNECTION_STATES.CONNECTING || this.state === CONNECTION_STATES.CONNECTED) {
      return;
    }

    console.log(`WebSocket: Connecting to ${this.url}`);
    this.setState(CONNECTION_STATES.CONNECTING);

    try {
      this.ws = new WebSocket(this.url);
      this.setupEventHandlers();
    } catch (error) {
      console.error('WebSocket: Connection failed', error);
      this.handleError(error);
    }
  }

  /**
   * Setup WebSocket event handlers
   */
  setupEventHandlers() {
    if (!this.ws) return;

    this.ws.onopen = () => {
      console.log('WebSocket: Connection established');
      this.setState(CONNECTION_STATES.CONNECTED);
      this.reconnectAttempts = 0;
      this.startHeartbeat();
    };

    this.ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        this.handleMessage(message);
      } catch (error) {
        console.error('WebSocket: Failed to parse message', error);
      }
    };

    this.ws.onclose = (event) => {
      console.log('WebSocket: Connection closed', event.code, event.reason);
      this.setState(CONNECTION_STATES.DISCONNECTED);
      this.stopHeartbeat();

      if (this.options.autoReconnect && !event.wasClean) {
        this.scheduleReconnect();
      }
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket: Connection error', error);
      this.handleError(error);
    };
  }

  /**
   * Handle incoming messages
   */
  handleMessage(message) {
    console.log('WebSocket: Message received', message);

    // Handle pong responses
    if (message.type === MESSAGE_TYPES.PONG) {
      this.lastHeartbeat = Date.now();
      return;
    }

    // Notify all message listeners
    this.listeners.message.forEach(callback => {
      try {
        callback(message);
      } catch (error) {
        console.error('WebSocket: Error in message handler', error);
      }
    });
  }

  /**
   * Send message through WebSocket
   */
  send(message) {
    if (this.state !== CONNECTION_STATES.CONNECTED) {
      console.warn('WebSocket: Cannot send message, not connected');
      return false;
    }

    try {
      const data = typeof message === 'string' ? message : JSON.stringify(message);
      this.ws.send(data);
      return true;
    } catch (error) {
      console.error('WebSocket: Failed to send message', error);
      return false;
    }
  }

  /**
   * Send ping to keep connection alive
   */
  ping() {
    return this.send({ type: MESSAGE_TYPES.PING, timestamp: new Date().toISOString() });
  }

  /**
   * Start heartbeat mechanism
   */
  startHeartbeat() {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
    }

    this.heartbeatInterval = setInterval(() => {
      if (this.state === CONNECTION_STATES.CONNECTED) {
        this.ping();
      }
    }, this.options.heartbeatInterval);
  }

  /**
   * Stop heartbeat mechanism
   */
  stopHeartbeat() {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }
  }

  /**
   * Schedule reconnection attempt
   */
  scheduleReconnect() {
    if (this.reconnectAttempts >= this.options.maxReconnectAttempts) {
      console.error('WebSocket: Max reconnection attempts reached');
      this.setState(CONNECTION_STATES.FAILED);
      return;
    }

    this.reconnectAttempts++;
    console.log(`WebSocket: Scheduling reconnect attempt ${this.reconnectAttempts}`);
    this.setState(CONNECTION_STATES.RECONNECTING);

    this.reconnectTimeout = setTimeout(() => {
      this.connect();
    }, this.options.reconnectInterval);
  }

  /**
   * Handle connection errors
   */
  handleError(error) {
    this.listeners.error.forEach(callback => {
      try {
        callback(error);
      } catch (err) {
        console.error('WebSocket: Error in error handler', err);
      }
    });
  }

  /**
   * Set connection state and notify listeners
   */
  setState(newState) {
    if (this.state !== newState) {
      const oldState = this.state;
      this.state = newState;

      console.log(`WebSocket: State changed from ${oldState} to ${newState}`);

      this.listeners.stateChange.forEach(callback => {
        try {
          callback(newState, oldState);
        } catch (error) {
          console.error('WebSocket: Error in state change handler', error);
        }
      });
    }
  }

  /**
   * Add event listener
   */
  addEventListener(event, callback) {
    if (this.listeners[event]) {
      this.listeners[event].add(callback);
    }
  }

  /**
   * Remove event listener
   */
  removeEventListener(event, callback) {
    if (this.listeners[event]) {
      this.listeners[event].delete(callback);
    }
  }

  /**
   * Close connection
   */
  close() {
    console.log('WebSocket: Closing connection');

    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
      this.reconnectTimeout = null;
    }

    this.stopHeartbeat();

    if (this.ws) {
      this.ws.close(1000, 'Connection closed by client');
      this.ws = null;
    }

    this.setState(CONNECTION_STATES.DISCONNECTED);
  }

  /**
   * Get current connection state
   */
  getState() {
    return this.state;
  }

  /**
   * Check if connected
   */
  isConnected() {
    return this.state === CONNECTION_STATES.CONNECTED;
  }
}

/**
 * WebSocket Service Factory
 */
export class WebSocketService {
  constructor() {
    this.connections = new Map();
  }

  /**
   * Connect to workflow-specific WebSocket
   */
  connectToWorkflow(adwId, options = {}) {
    const url = `${WS_BASE_URL}/ws/workflows/${adwId}`;
    const connectionKey = `workflow:${adwId}`;

    if (this.connections.has(connectionKey)) {
      return this.connections.get(connectionKey);
    }

    const connection = new WebSocketConnection(url, options);
    this.connections.set(connectionKey, connection);

    return connection;
  }

  /**
   * Connect to global WebSocket (all workflow updates)
   */
  connectToGlobal(options = {}) {
    const url = `${WS_BASE_URL}/ws/global`;
    const connectionKey = 'global';

    if (this.connections.has(connectionKey)) {
      return this.connections.get(connectionKey);
    }

    const connection = new WebSocketConnection(url, options);
    this.connections.set(connectionKey, connection);

    return connection;
  }

  /**
   * Disconnect from workflow WebSocket
   */
  disconnectFromWorkflow(adwId) {
    const connectionKey = `workflow:${adwId}`;
    const connection = this.connections.get(connectionKey);

    if (connection) {
      connection.close();
      this.connections.delete(connectionKey);
    }
  }

  /**
   * Disconnect from global WebSocket
   */
  disconnectFromGlobal() {
    const connectionKey = 'global';
    const connection = this.connections.get(connectionKey);

    if (connection) {
      connection.close();
      this.connections.delete(connectionKey);
    }
  }

  /**
   * Disconnect all connections
   */
  disconnectAll() {
    console.log('WebSocket: Disconnecting all connections');
    this.connections.forEach(connection => connection.close());
    this.connections.clear();
  }

  /**
   * Get connection status
   */
  getConnectionStatus() {
    const status = {};
    this.connections.forEach((connection, key) => {
      status[key] = {
        state: connection.getState(),
        connected: connection.isConnected(),
      };
    });
    return status;
  }
}

// Create singleton instance
const webSocketService = new WebSocketService();

// Cleanup connections when page unloads
if (typeof window !== 'undefined') {
  window.addEventListener('beforeunload', () => {
    webSocketService.disconnectAll();
  });
}

export default webSocketService;