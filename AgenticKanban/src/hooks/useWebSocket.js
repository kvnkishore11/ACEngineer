/**
 * React Hook for WebSocket Integration
 * Provides real-time updates for workflow tasks
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import webSocketService, { CONNECTION_STATES, MESSAGE_TYPES } from '../services/websocketService';

/**
 * Hook for connecting to a specific workflow WebSocket
 * @param {string} adwId - ADW identifier
 * @param {Object} options - WebSocket options
 * @returns {Object} WebSocket state and utilities
 */
export const useWorkflowWebSocket = (adwId, options = {}) => {
  const [connectionState, setConnectionState] = useState(CONNECTION_STATES.DISCONNECTED);
  const [lastMessage, setLastMessage] = useState(null);
  const [error, setError] = useState(null);
  const [messageHistory, setMessageHistory] = useState([]);

  const connectionRef = useRef(null);
  const messageHandlerRef = useRef(null);
  const stateHandlerRef = useRef(null);
  const errorHandlerRef = useRef(null);

  // Message handler
  const handleMessage = useCallback((message) => {
    console.log('useWebSocket: Message received for workflow', adwId, message);
    setLastMessage(message);
    setMessageHistory(prev => [...prev, { ...message, receivedAt: Date.now() }]);
  }, [adwId]);

  // State change handler
  const handleStateChange = useCallback((newState) => {
    console.log('useWebSocket: State changed for workflow', adwId, newState);
    setConnectionState(newState);

    if (newState === CONNECTION_STATES.CONNECTED) {
      setError(null);
    }
  }, [adwId]);

  // Error handler
  const handleError = useCallback((error) => {
    console.error('useWebSocket: Error for workflow', adwId, error);
    setError(error);
  }, [adwId]);

  // Store handlers in refs to prevent effect dependencies
  messageHandlerRef.current = handleMessage;
  stateHandlerRef.current = handleStateChange;
  errorHandlerRef.current = handleError;

  // Connect to WebSocket
  useEffect(() => {
    if (!adwId) return;

    console.log('useWebSocket: Connecting to workflow', adwId);

    const connection = webSocketService.connectToWorkflow(adwId, {
      autoReconnect: true,
      ...options,
    });

    connectionRef.current = connection;

    // Add event listeners
    const messageHandler = (message) => messageHandlerRef.current(message);
    const stateHandler = (newState) => stateHandlerRef.current(newState);
    const errorHandler = (error) => errorHandlerRef.current(error);

    connection.addEventListener('message', messageHandler);
    connection.addEventListener('stateChange', stateHandler);
    connection.addEventListener('error', errorHandler);

    // Set initial state
    setConnectionState(connection.getState());

    // Cleanup function
    return () => {
      console.log('useWebSocket: Cleaning up workflow connection', adwId);

      connection.removeEventListener('message', messageHandler);
      connection.removeEventListener('stateChange', stateHandler);
      connection.removeEventListener('error', errorHandler);

      webSocketService.disconnectFromWorkflow(adwId);
      connectionRef.current = null;
    };
  }, [adwId, JSON.stringify(options)]);

  // Send message function
  const sendMessage = useCallback((message) => {
    const connection = connectionRef.current;
    if (connection && connection.isConnected()) {
      return connection.send(message);
    }
    console.warn('useWebSocket: Cannot send message, not connected');
    return false;
  }, []);

  // Reconnect function
  const reconnect = useCallback(() => {
    const connection = connectionRef.current;
    if (connection) {
      connection.connect();
    }
  }, []);

  return {
    // Connection state
    connectionState,
    isConnected: connectionState === CONNECTION_STATES.CONNECTED,
    isConnecting: connectionState === CONNECTION_STATES.CONNECTING,
    isReconnecting: connectionState === CONNECTION_STATES.RECONNECTING,

    // Messages
    lastMessage,
    messageHistory,

    // Error handling
    error,

    // Actions
    sendMessage,
    reconnect,
  };
};

/**
 * Hook for connecting to global workflow updates
 * @param {Object} options - WebSocket options
 * @returns {Object} WebSocket state and utilities
 */
export const useGlobalWebSocket = (options = {}) => {
  const [connectionState, setConnectionState] = useState(CONNECTION_STATES.DISCONNECTED);
  const [lastMessage, setLastMessage] = useState(null);
  const [error, setError] = useState(null);
  const [messageHistory, setMessageHistory] = useState([]);

  const connectionRef = useRef(null);
  const messageHandlerRef = useRef(null);
  const stateHandlerRef = useRef(null);
  const errorHandlerRef = useRef(null);

  // Message handler
  const handleMessage = useCallback((message) => {
    console.log('useWebSocket: Global message received', message);
    setLastMessage(message);
    setMessageHistory(prev => [...prev, { ...message, receivedAt: Date.now() }]);
  }, []);

  // State change handler
  const handleStateChange = useCallback((newState) => {
    console.log('useWebSocket: Global state changed', newState);
    setConnectionState(newState);

    if (newState === CONNECTION_STATES.CONNECTED) {
      setError(null);
    }
  }, []);

  // Error handler
  const handleError = useCallback((error) => {
    console.error('useWebSocket: Global error', error);
    setError(error);
  }, []);

  // Store handlers in refs
  messageHandlerRef.current = handleMessage;
  stateHandlerRef.current = handleStateChange;
  errorHandlerRef.current = handleError;

  // Connect to WebSocket
  useEffect(() => {
    console.log('useWebSocket: Connecting to global WebSocket');

    const connection = webSocketService.connectToGlobal({
      autoReconnect: true,
      ...options,
    });

    connectionRef.current = connection;

    // Add event listeners
    const messageHandler = (message) => messageHandlerRef.current(message);
    const stateHandler = (newState) => stateHandlerRef.current(newState);
    const errorHandler = (error) => errorHandlerRef.current(error);

    connection.addEventListener('message', messageHandler);
    connection.addEventListener('stateChange', stateHandler);
    connection.addEventListener('error', errorHandler);

    // Set initial state
    setConnectionState(connection.getState());

    // Cleanup function
    return () => {
      console.log('useWebSocket: Cleaning up global connection');

      connection.removeEventListener('message', messageHandler);
      connection.removeEventListener('stateChange', stateHandler);
      connection.removeEventListener('error', errorHandler);

      webSocketService.disconnectFromGlobal();
      connectionRef.current = null;
    };
  }, [JSON.stringify(options)]);

  // Send message function
  const sendMessage = useCallback((message) => {
    const connection = connectionRef.current;
    if (connection && connection.isConnected()) {
      return connection.send(message);
    }
    console.warn('useWebSocket: Cannot send message, not connected');
    return false;
  }, []);

  // Reconnect function
  const reconnect = useCallback(() => {
    const connection = connectionRef.current;
    if (connection) {
      connection.connect();
    }
  }, []);

  return {
    // Connection state
    connectionState,
    isConnected: connectionState === CONNECTION_STATES.CONNECTED,
    isConnecting: connectionState === CONNECTION_STATES.CONNECTING,
    isReconnecting: connectionState === CONNECTION_STATES.RECONNECTING,

    // Messages
    lastMessage,
    messageHistory,

    // Error handling
    error,

    // Actions
    sendMessage,
    reconnect,
  };
};

/**
 * Hook for filtering messages by type
 * @param {Array} messageHistory - Array of messages
 * @param {string|Array} messageTypes - Message type(s) to filter
 * @returns {Array} Filtered messages
 */
export const useFilteredMessages = (messageHistory, messageTypes) => {
  return messageHistory.filter(message => {
    if (Array.isArray(messageTypes)) {
      return messageTypes.includes(message.type);
    }
    return message.type === messageTypes;
  });
};

/**
 * Hook for tracking task progress from WebSocket messages
 * @param {Array} messageHistory - Array of messages
 * @returns {Object} Progress tracking data
 */
export const useTaskProgress = (messageHistory) => {
  const [progress, setProgress] = useState({
    stage: null,
    percentage: 0,
    status: 'pending',
    lastUpdate: null,
  });

  useEffect(() => {
    // Find the latest progress or status update
    const relevantMessages = messageHistory.filter(message =>
      message.type === MESSAGE_TYPES.PROGRESS_UPDATE ||
      message.type === MESSAGE_TYPES.STATUS_UPDATE ||
      message.type === MESSAGE_TYPES.STAGE_UPDATE
    );

    if (relevantMessages.length === 0) return;

    const latestMessage = relevantMessages[relevantMessages.length - 1];
    const data = latestMessage.data || {};

    setProgress(prev => ({
      stage: data.current_stage || data.stage || prev.stage,
      percentage: data.progress || prev.percentage,
      status: data.status || prev.status,
      lastUpdate: latestMessage.timestamp || latestMessage.receivedAt,
    }));
  }, [messageHistory]);

  return progress;
};

// Export MESSAGE_TYPES and CONNECTION_STATES for convenience
export { MESSAGE_TYPES, CONNECTION_STATES };