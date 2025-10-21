import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import adwService from '../services/adwService';
import localStorageService from '../services/localStorage';
import stageProgressionService from '../services/stageProgressionService';
import apiService, { APIError, NetworkError } from '../services/apiService';
import webSocketService from '../services/websocketService';
import {
  generateAdwId,
  generateWorkflowCommand,
  createTaskData,
  pollWorkflowState,
  updateTaskFromState
} from '../utils/commandGenerator';
import {
  executeWorkflow,
  isAutoExecutionSupported,
  getExecutionConfig,
  getExecutionStatus
} from '../utils/workflowExecutor';

// Work item types
export const WORK_ITEM_TYPES = {
  FEATURE: 'feature',
  CHORE: 'chore',
  BUG: 'bug',
  PATCH: 'patch'
};

// Available stages for queueing
export const QUEUEABLE_STAGES = [
  { id: 'plan', name: 'Plan', color: 'blue' },
  { id: 'implement', name: 'Implement', color: 'yellow' },
  { id: 'test', name: 'Test', color: 'green' },
  { id: 'review', name: 'Review', color: 'purple' },
  { id: 'document', name: 'Document', color: 'indigo' },
  { id: 'pr', name: 'PR', color: 'pink' }
];

const initialState = {
  // Project management
  selectedProject: null,
  availableProjects: [],

  // Task management
  tasks: [],
  taskIdCounter: 1,

  // Kanban board configuration
  stages: [
    { id: 'backlog', name: 'Backlog', color: 'gray' },
    { id: 'plan', name: 'Plan', color: 'blue' },
    { id: 'build', name: 'Build', color: 'yellow' },
    { id: 'test', name: 'Test', color: 'green' },
    { id: 'review', name: 'Review', color: 'purple' },
    { id: 'document', name: 'Document', color: 'indigo' },
    { id: 'pr', name: 'PR', color: 'pink' },
    { id: 'errored', name: 'Errored', color: 'red' },
  ],

  // ADW pipeline configurations
  availablePipelines: adwService.getAllPipelines(),

  // UI state
  showTaskInput: false,
  selectedTaskId: null,
  isLoading: false,
  error: null,

  // Automatic execution state
  executionConfig: null, // Will be loaded from localStorage
  executingTasks: new Map(), // Track tasks currently executing
  activePollingIntervals: new Map(), // Track polling intervals by adw_id

  // Modal state (for fallback to manual execution)
  showCommandModal: false,
  currentCommand: null,
  currentTaskData: null,

  // API + WebSocket integration state
  apiAvailable: null, // null = not checked, true/false = checked
  webSocketConnections: new Map(), // Track WebSocket connections by adwId
  globalWebSocketConnected: false,
  apiMode: true, // true = use API, false = fallback to file-based
};

export const useKanbanStore = create()(
  devtools(
    persist(
      (set, get) => ({
        ...initialState,

        // Project actions
        selectProject: (project) => {
          set({ selectedProject: project }, false, 'selectProject');
        },

        addProject: (project) => {
          set((state) => ({
            availableProjects: [...state.availableProjects, project],
          }), false, 'addProject');
        },

        // Task actions
        createTask: (taskData) => {
          // Generate dynamic pipeline name based on queuedStages
          const generatePipelineName = (queuedStages) => {
            if (!queuedStages || queuedStages.length === 0) {
              return 'adw_unknown';
            }
            return `adw_${queuedStages.join('_')}`;
          };

          const dynamicPipelineId = generatePipelineName(taskData.queuedStages);

          const newTask = {
            id: get().taskIdCounter,
            title: taskData.title || '', // Optional title
            description: taskData.description,
            workItemType: taskData.workItemType || WORK_ITEM_TYPES.FEATURE,
            queuedStages: taskData.queuedStages || [],
            pipelineId: dynamicPipelineId, // Dynamic pipeline name based on stages
            pipelineIdStatic: taskData.pipelineId, // Keep static pipelineId for backward compatibility
            stage: 'backlog',
            substage: 'initializing',
            progress: 0,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
            logs: [],
            metadata: {},
            images: taskData.images || [], // Support for uploaded images
          };

          set((state) => ({
            tasks: [...state.tasks, newTask],
            taskIdCounter: state.taskIdCounter + 1,
            showTaskInput: false,
          }), false, 'createTask');

          return newTask;
        },

        updateTask: (taskId, updates) => {
          set((state) => ({
            tasks: state.tasks.map(task =>
              task.id === taskId
                ? { ...task, ...updates, updatedAt: new Date().toISOString() }
                : task
            ),
          }), false, 'updateTask');
        },

        deleteTask: (taskId) => {
          set((state) => ({
            tasks: state.tasks.filter(task => task.id !== taskId),
            selectedTaskId: state.selectedTaskId === taskId ? null : state.selectedTaskId,
          }), false, 'deleteTask');
        },

        moveTaskToStage: (taskId, newStage) => {
          set((state) => ({
            tasks: state.tasks.map(task =>
              task.id === taskId
                ? {
                    ...task,
                    stage: newStage,
                    substage: 'initializing',
                    progress: 0,
                    updatedAt: new Date().toISOString()
                  }
                : task
            ),
          }), false, 'moveTaskToStage');
        },

        updateTaskProgress: (taskId, substage, progress) => {
          set((state) => ({
            tasks: state.tasks.map(task =>
              task.id === taskId
                ? {
                    ...task,
                    substage,
                    progress,
                    updatedAt: new Date().toISOString()
                  }
                : task
            ),
          }), false, 'updateTaskProgress');
        },

        addTaskLog: (taskId, logEntry) => {
          set((state) => ({
            tasks: state.tasks.map(task =>
              task.id === taskId
                ? {
                    ...task,
                    logs: [...task.logs, {
                      ...logEntry,
                      timestamp: new Date().toISOString(),
                    }],
                    updatedAt: new Date().toISOString()
                  }
                : task
            ),
          }), false, 'addTaskLog');
        },

        // Enhanced error handling
        handleError: (error, context = '') => {
          console.error(`KanbanStore Error${context ? ` (${context})` : ''}:`, error);

          const errorMessage = error instanceof Error ? error.message : String(error);
          const errorDetails = {
            message: errorMessage,
            context,
            timestamp: new Date().toISOString(),
            stack: error instanceof Error ? error.stack : undefined,
          };

          set({
            error: errorMessage,
            lastError: errorDetails,
          }, false, 'handleError');

          // Return false to indicate operation failed
          return false;
        },

        // Retry mechanism for failed operations
        retryOperation: async (operation, maxRetries = 3, delay = 1000) => {
          for (let attempt = 1; attempt <= maxRetries; attempt++) {
            try {
              const result = await operation();
              return result;
            } catch (error) {
              if (attempt === maxRetries) {
                get().handleError(error, `Failed after ${maxRetries} attempts`);
                throw error;
              }

              console.warn(`Operation failed (attempt ${attempt}/${maxRetries}):`, error);
              await new Promise(resolve => setTimeout(resolve, delay * attempt));
            }
          }
        },

        // Validation helpers
        validateTask: (task) => {
          const errors = [];

          // Title is now optional, but if provided, must be reasonable length
          if (task.title && task.title.length > 100) {
            errors.push('Task title must be less than 100 characters');
          }

          // Description is required
          if (!task.description || task.description.trim().length === 0) {
            errors.push('Task description is required');
          }

          if (task.description && task.description.length > 2000) {
            errors.push('Task description must be less than 2000 characters');
          }

          // Work item type validation
          if (!task.workItemType || !Object.values(WORK_ITEM_TYPES).includes(task.workItemType)) {
            errors.push('Valid work item type is required (Feature, Chore, Bug, or Patch)');
          }

          // Queued stages validation
          if (task.queuedStages && !Array.isArray(task.queuedStages)) {
            errors.push('Queued stages must be an array');
          }

          if (task.queuedStages && task.queuedStages.length === 0) {
            errors.push('At least one stage must be selected');
          }

          // Validate each queued stage
          if (task.queuedStages && task.queuedStages.length > 0) {
            const validStageIds = QUEUEABLE_STAGES.map(s => s.id);
            const invalidStages = task.queuedStages.filter(stage => !validStageIds.includes(stage));
            if (invalidStages.length > 0) {
              errors.push(`Invalid stages selected: ${invalidStages.join(', ')}`);
            }
          }

          return {
            isValid: errors.length === 0,
            errors,
          };
        },

        validateProject: (project) => {
          const errors = [];

          if (!project.name || project.name.trim().length === 0) {
            errors.push('Project name is required');
          }

          if (!project.path || project.path.trim().length === 0) {
            errors.push('Project path is required');
          }

          // Simulate validation of project structure
          if (!project.hasAgentics) {
            errors.push('Project must have agentics/ directory');
          }

          if (!project.hasClaude) {
            errors.push('Project must have .claude/ directory');
          }

          return {
            isValid: errors.length === 0,
            errors,
          };
        },

        // UI actions
        toggleTaskInput: () => {
          set((state) => ({ showTaskInput: !state.showTaskInput }), false, 'toggleTaskInput');
        },

        selectTask: (taskId) => {
          set({ selectedTaskId: taskId }, false, 'selectTask');
        },

        setLoading: (isLoading) => {
          set({ isLoading }, false, 'setLoading');
        },

        setError: (error) => {
          set({ error }, false, 'setError');
        },

        clearError: () => {
          set({ error: null }, false, 'clearError');
        },

        // API availability check
        checkAPIAvailability: async () => {
          const { apiAvailable } = get();

          // Return cached result if already checked
          if (apiAvailable !== null) {
            return apiAvailable;
          }

          try {
            const isAvailable = await apiService.utils.isAPIAvailable();
            set({ apiAvailable: isAvailable }, false, 'checkAPIAvailability');
            return isAvailable;
          } catch (error) {
            set({ apiAvailable: false }, false, 'checkAPIAvailabilityError');
            return false;
          }
        },

        // WebSocket connection management
        connectToWorkflowWebSocket: (adwId, taskId) => {
          try {
            const connection = webSocketService.connectToWorkflow(adwId);

            // Add message handler for this specific workflow
            connection.addEventListener('message', (message) => {
              get().handleWebSocketMessage(message, adwId, taskId);
            });

            // Add error handler
            connection.addEventListener('error', (error) => {
              console.error(`WebSocket error for workflow ${adwId}:`, error);
              get().addTaskLog(taskId, {
                level: 'error',
                message: `WebSocket connection error: ${error.message}`
              });
            });

            // Store connection reference
            set((state) => {
              const newConnections = new Map(state.webSocketConnections);
              newConnections.set(adwId, { connection, taskId });
              return { webSocketConnections: newConnections };
            }, false, 'connectToWorkflowWebSocket');

            return connection;
          } catch (error) {
            get().handleError(error, 'connectToWorkflowWebSocket');
            return null;
          }
        },

        // Handle WebSocket messages
        handleWebSocketMessage: (message, adwId, taskId) => {
          try {
            console.log('Received WebSocket message:', message);

            const { type, data } = message;

            switch (type) {
              case 'task_created':
                get().addTaskLog(taskId, {
                  level: 'info',
                  message: 'Task successfully submitted to orchestrator'
                });
                break;

              case 'status_update':
                get().updateTaskFromAPIResponse(taskId, data);
                break;

              case 'stage_update':
                get().updateTask(taskId, {
                  stage: get().mapAPIStageToKanbanStage(data.current_stage),
                  substage: data.current_stage,
                });
                get().addTaskLog(taskId, {
                  level: 'info',
                  message: `Stage updated to: ${data.current_stage}`
                });
                break;

              case 'progress_update':
                get().updateTaskProgress(taskId, data.stage, data.progress || 0);
                if (data.stage_result) {
                  get().addTaskLog(taskId, {
                    level: 'info',
                    message: `Stage ${data.stage} completed`,
                    details: data.stage_result
                  });
                }
                break;

              case 'task_cancelled':
                get().updateTask(taskId, {
                  status: 'cancelled',
                  stage: 'errored'
                });
                get().addTaskLog(taskId, {
                  level: 'warning',
                  message: 'Task was cancelled'
                });
                break;

              case 'connection_established':
                get().addTaskLog(taskId, {
                  level: 'info',
                  message: 'Real-time updates connected'
                });
                break;

              default:
                console.log('Unhandled WebSocket message type:', type);
            }
          } catch (error) {
            get().handleError(error, 'handleWebSocketMessage');
          }
        },

        // Disconnect from WebSocket
        disconnectFromWorkflowWebSocket: (adwId) => {
          const { webSocketConnections } = get();
          const connectionInfo = webSocketConnections.get(adwId);

          if (connectionInfo) {
            webSocketService.disconnectFromWorkflow(adwId);

            set((state) => {
              const newConnections = new Map(state.webSocketConnections);
              newConnections.delete(adwId);
              return { webSocketConnections: newConnections };
            }, false, 'disconnectFromWorkflowWebSocket');
          }
        },

        // Map API stage names to Kanban stage names
        mapAPIStageToKanbanStage: (apiStage) => {
          const stageMapping = {
            'plan': 'plan',
            'implement': 'build',
            'test': 'test',
            'deploy': 'pr',
            'completed': 'pr',
            'failed': 'errored',
            'cancelled': 'errored'
          };

          return stageMapping[apiStage] || 'backlog';
        },

        // Update task from API response data
        updateTaskFromAPIResponse: (taskId, apiData) => {
          const updates = {
            status: apiData.status,
            updatedAt: apiData.updated_at || new Date().toISOString()
          };

          if (apiData.current_stage) {
            updates.stage = get().mapAPIStageToKanbanStage(apiData.current_stage);
            updates.substage = apiData.current_stage;
          }

          if (apiData.result) {
            updates.metadata = {
              ...get().tasks.find(t => t.id === taskId)?.metadata,
              result: apiData.result
            };
          }

          if (apiData.error_message) {
            updates.stage = 'errored';
            get().addTaskLog(taskId, {
              level: 'error',
              message: apiData.error_message
            });
          }

          if (apiData.status === 'completed') {
            updates.stage = 'pr';
            updates.progress = 100;
            get().addTaskLog(taskId, {
              level: 'success',
              message: 'Task completed successfully!'
            });
          }

          get().updateTask(taskId, updates);
        },

        // API + WebSocket workflow execution
        createTaskWithCommand: async (taskInput) => {
          try {
            // Check if API is available
            const apiAvailable = await get().checkAPIAvailability();

            if (apiAvailable && get().apiMode) {
              // Use new API + WebSocket architecture
              return await get().createTaskWithAPI(taskInput);
            } else {
              // Fallback to file-based system
              return await get().createTaskWithFileSystem(taskInput);
            }
          } catch (error) {
            get().handleError(error, 'createTaskWithCommand');
            throw error;
          }
        },

        // New API-based task creation
        createTaskWithAPI: async (taskInput) => {
          try {
            // Convert taskInput to API format
            const apiTaskData = {
              title: taskInput.title || `${taskInput.workItemType} Task`,
              description: taskInput.description,
              task_type: taskInput.workItemType || 'feature',
              stages: taskInput.queuedStages || ['plan', 'implement', 'test']
            };

            // Create task via API
            const apiResponse = await apiService.workflow.create(apiTaskData);

            // Create local task based on API response
            const newTask = {
              id: get().taskIdCounter,
              title: apiResponse.title,
              description: apiResponse.description,
              workItemType: apiResponse.task_type,
              queuedStages: apiResponse.stages,
              pipelineId: `adw_${apiResponse.stages.join('_')}`,
              stage: 'backlog',
              status: apiResponse.status,
              progress: 0,
              createdAt: apiResponse.created_at,
              updatedAt: apiResponse.updated_at,
              logs: [{
                level: 'info',
                message: 'Task created via API',
                timestamp: new Date().toISOString()
              }],
              metadata: {
                adwId: apiResponse.adw_id,
                apiTaskId: apiResponse.id,
                executionMode: 'api',
                apiAvailable: true
              },
              images: taskInput.images || []
            };

            // Add task to store
            set((state) => ({
              tasks: [...state.tasks, newTask],
              taskIdCounter: state.taskIdCounter + 1,
              showTaskInput: false,
            }), false, 'createTaskWithAPI');

            // Connect to WebSocket for real-time updates
            get().connectToWorkflowWebSocket(apiResponse.adw_id, newTask.id);

            return {
              task: newTask,
              adwId: apiResponse.adw_id,
              autoExecuted: true,
              apiResponse
            };
          } catch (error) {
            if (error instanceof APIError || error instanceof NetworkError) {
              console.warn('API creation failed, falling back to file system:', error);
              // Fallback to file-based system
              set({ apiMode: false }, false, 'apiFailureFallback');
              return await get().createTaskWithFileSystem(taskInput);
            }
            throw error;
          }
        },

        // Fallback file-based task creation
        createTaskWithFileSystem: async (taskInput) => {
          try {
            const { selectedProject } = get();
            if (!selectedProject || !selectedProject.handle) {
              throw new Error('No project selected or project handle missing');
            }

            // Generate ADW ID
            const adwId = generateAdwId();

            // Create task data for ADW workflow
            const taskData = createTaskData(taskInput, adwId);

            // Create task in Kanban first
            const newTask = {
              id: get().taskIdCounter,
              ...taskData,
              stage: 'backlog',
              status: 'initializing',
              progress: 0,
              createdAt: new Date().toISOString(),
              updatedAt: new Date().toISOString(),
              logs: [{
                level: 'info',
                message: 'Task created via file system (fallback)',
                timestamp: new Date().toISOString()
              }],
              metadata: {
                adwId,
                projectHandle: selectedProject.handle,
                executionMode: 'file_system',
                apiAvailable: false
              }
            };

            set((state) => ({
              tasks: [...state.tasks, newTask],
              taskIdCounter: state.taskIdCounter + 1,
              showTaskInput: false,
            }), false, 'createTaskWithFileSystem');

            // Check execution configuration
            const config = get().getExecutionConfig();
            const autoExecutionSupported = await isAutoExecutionSupported(selectedProject.handle);

            if (config.autoExecute && autoExecutionSupported) {
              // Execute automatically using file system
              await get().executeTaskAutomatically(newTask.id, taskData, selectedProject.handle);
            } else {
              // Fall back to manual execution
              const command = generateWorkflowCommand(taskData, selectedProject.handle);
              get().updateTask(newTask.id, {
                status: 'waiting_for_manual_execution',
                metadata: {
                  ...newTask.metadata,
                  command: command.full,
                  executionMode: 'manual',
                  requiresManualExecution: true
                }
              });

              if (config.fallbackToManual) {
                // Show manual command (will be handled by CommandDisplay component)
                set({
                  showCommandModal: true,
                  currentCommand: command,
                  currentTaskData: taskData,
                }, false, 'fallbackToManual');
              }
            }

            return { task: newTask, adwId, autoExecuted: config.autoExecute && autoExecutionSupported };
          } catch (error) {
            get().handleError(error, 'createTaskWithFileSystem');
            throw error;
          }
        },

        // Execution configuration management
        getExecutionConfig: () => {
          const state = get();
          if (state.executionConfig) {
            return state.executionConfig;
          }

          // Load from localStorage and cache
          const config = getExecutionConfig();
          set({ executionConfig: config }, false, 'loadExecutionConfig');
          return config;
        },

        updateExecutionConfig: (newConfig) => {
          const mergedConfig = { ...get().getExecutionConfig(), ...newConfig };
          set({ executionConfig: mergedConfig }, false, 'updateExecutionConfig');

          // Save to localStorage via utility
          return get().saveExecutionConfig(mergedConfig);
        },

        saveExecutionConfig: (config) => {
          try {
            localStorage.setItem('adw_execution_config', JSON.stringify(config));
            return true;
          } catch (error) {
            get().handleError(error, 'saveExecutionConfig');
            return false;
          }
        },

        // Automatic execution functions
        executeTaskAutomatically: async (taskId, taskData, projectHandle) => {
          try {
            const adwId = taskData.adw_id;

            // Mark task as executing
            set((state) => {
              const newExecutingTasks = new Map(state.executingTasks);
              newExecutingTasks.set(adwId, {
                taskId,
                startTime: Date.now(),
                status: 'executing'
              });
              return { executingTasks: newExecutingTasks };
            }, false, 'markTaskExecuting');

            // Update task status
            get().updateTask(taskId, {
              status: 'executing',
              stage: 'plan', // Move to first stage
              logs: [{
                level: 'info',
                message: 'Starting automatic workflow execution...',
                timestamp: new Date().toISOString()
              }]
            });

            // Execute the workflow
            const result = await executeWorkflow(taskData, projectHandle);

            if (result.success) {
              // Update task with success
              get().updateTask(taskId, {
                status: 'executing',
                logs: [...(get().tasks.find(t => t.id === taskId)?.logs || []), {
                  level: 'success',
                  message: 'Workflow execution initiated successfully',
                  timestamp: new Date().toISOString()
                }]
              });

              // Start polling for state updates
              get().startPolling(adwId, projectHandle);

              return { success: true, adwId };
            } else {
              // Handle execution failure
              get().updateTask(taskId, {
                status: 'execution_failed',
                stage: 'errored',
                logs: [...(get().tasks.find(t => t.id === taskId)?.logs || []), {
                  level: 'error',
                  message: `Execution failed: ${result.error}`,
                  timestamp: new Date().toISOString()
                }]
              });

              // Remove from executing tasks
              set((state) => {
                const newExecutingTasks = new Map(state.executingTasks);
                newExecutingTasks.delete(adwId);
                return { executingTasks: newExecutingTasks };
              }, false, 'removeFailedTask');

              return { success: false, error: result.error };
            }
          } catch (error) {
            get().handleError(error, 'executeTaskAutomatically');

            // Update task with error
            get().updateTask(taskId, {
              status: 'execution_failed',
              stage: 'errored',
              logs: [...(get().tasks.find(t => t.id === taskId)?.logs || []), {
                level: 'error',
                message: `Execution error: ${error.message}`,
                timestamp: new Date().toISOString()
              }]
            });

            throw error;
          }
        },

        getExecutionStatus: async (adwId, projectHandle) => {
          try {
            return await getExecutionStatus(adwId, projectHandle);
          } catch (error) {
            get().handleError(error, 'getExecutionStatus');
            return { found: false, status: 'error', error: error.message };
          }
        },

        isTaskExecuting: (adwId) => {
          return get().executingTasks.has(adwId);
        },

        getExecutingTasks: () => {
          return Array.from(get().executingTasks.entries()).map(([adwId, info]) => ({
            adwId,
            ...info
          }));
        },

        showCommandModal: (command, taskData) => {
          set({
            showCommandModal: true,
            currentCommand: command,
            currentTaskData: taskData,
          }, false, 'showCommandModal');
        },

        hideCommandModal: () => {
          set({
            showCommandModal: false,
            currentCommand: null,
            currentTaskData: null,
          }, false, 'hideCommandModal');
        },

        startPolling: (adwId, projectHandle) => {
          try {
            // Stop any existing polling for this ADW ID
            get().stopPolling(adwId);

            // Start new polling
            const pollInterval = pollWorkflowState(
              adwId,
              projectHandle,
              (adwId, state) => get().updateTaskFromAdwState(adwId, state)
            );

            // Store the interval
            set((state) => {
              const newIntervals = new Map(state.activePollingIntervals);
              newIntervals.set(adwId, pollInterval);
              return { activePollingIntervals: newIntervals };
            }, false, 'startPolling');

            return pollInterval;
          } catch (error) {
            get().handleError(error, 'startPolling');
            return null;
          }
        },

        stopPolling: (adwId) => {
          const state = get();
          const pollInterval = state.activePollingIntervals.get(adwId);

          if (pollInterval) {
            clearInterval(pollInterval);

            set((state) => {
              const newIntervals = new Map(state.activePollingIntervals);
              newIntervals.delete(adwId);
              return { activePollingIntervals: newIntervals };
            }, false, 'stopPolling');
          }
        },

        stopAllPolling: () => {
          const { activePollingIntervals } = get();

          // Clear all intervals
          activePollingIntervals.forEach((interval) => {
            clearInterval(interval);
          });

          set({ activePollingIntervals: new Map() }, false, 'stopAllPolling');
        },

        updateTaskFromAdwState: (adwId, adwState) => {
          try {
            const taskUpdate = updateTaskFromState(adwState);

            set((state) => ({
              tasks: state.tasks.map(task =>
                task.metadata?.adwId === adwId
                  ? {
                      ...task,
                      ...taskUpdate,
                      updatedAt: new Date().toISOString()
                    }
                  : task
              ),
            }), false, 'updateTaskFromAdwState');

            // Stop polling if workflow completed or failed
            if (adwState.overall_status === 'completed' || adwState.overall_status === 'failed') {
              get().stopPolling(adwId);
            }
          } catch (error) {
            get().handleError(error, 'updateTaskFromAdwState');
          }
        },

        findTaskByAdwId: (adwId) => {
          const { tasks } = get();
          return tasks.find(task => task.metadata?.adwId === adwId);
        },

        // Utility actions
        getTasksByStage: (stage) => {
          return get().tasks.filter(task => task.stage === stage);
        },

        getTasksForCurrentProject: () => {
          const { tasks, selectedProject } = get();
          return selectedProject
            ? tasks.filter(task => task.projectId === selectedProject.id)
            : tasks;
        },

        getPipelineById: (pipelineId) => {
          return adwService.getPipelineById(pipelineId);
        },

        // ADW Pipeline management
        refreshPipelines: () => {
          set({ availablePipelines: adwService.getAllPipelines() }, false, 'refreshPipelines');
        },

        createCustomPipeline: (pipelineData) => {
          try {
            const newPipeline = adwService.createCustomPipeline(pipelineData);
            set({ availablePipelines: adwService.getAllPipelines() }, false, 'createCustomPipeline');
            return newPipeline;
          } catch (error) {
            set({ error: error.message }, false, 'createCustomPipelineError');
            throw error;
          }
        },

        getNextStageInPipeline: (pipelineId, currentStage) => {
          try {
            return adwService.getNextStage(pipelineId, currentStage);
          } catch (error) {
            console.error('Error getting next stage:', error);
            return null;
          }
        },

        calculateTaskProgress: (task) => {
          try {
            return adwService.calculatePipelineProgress(task.pipelineId, task.stage, task.substage);
          } catch (error) {
            console.error('Error calculating progress:', error);
            return task.progress || 0;
          }
        },

        // Automatic stage progression
        startTaskProgression: (taskId) => {
          const task = get().tasks.find(t => t.id === taskId);
          if (!task) {
            set({ error: 'Task not found for progression' }, false, 'startTaskProgressionError');
            return false;
          }

          try {
            stageProgressionService.startProgression(taskId, { getState: get });

            // Update task metadata to indicate active progression
            set((state) => ({
              tasks: state.tasks.map(t =>
                t.id === taskId
                  ? { ...t, metadata: { ...t.metadata, autoProgress: true } }
                  : t
              ),
            }), false, 'startTaskProgression');

            return true;
          } catch (error) {
            set({ error: `Failed to start progression: ${error.message}` }, false, 'startTaskProgressionError');
            return false;
          }
        },

        stopTaskProgression: (taskId) => {
          stageProgressionService.stopProgression(taskId);

          // Update task metadata
          set((state) => ({
            tasks: state.tasks.map(t =>
              t.id === taskId
                ? { ...t, metadata: { ...t.metadata, autoProgress: false } }
                : t
            ),
          }), false, 'stopTaskProgression');
        },

        pauseTaskProgression: (taskId) => {
          stageProgressionService.pauseProgression(taskId);
        },

        resumeTaskProgression: (taskId) => {
          stageProgressionService.resumeProgression(taskId);
        },

        recoverTaskFromError: async (taskId, targetStage = null) => {
          try {
            await stageProgressionService.recoverFromError(taskId, { getState: get }, targetStage);
            return true;
          } catch (error) {
            set({ error: `Recovery failed: ${error.message}` }, false, 'recoverTaskFromErrorError');
            return false;
          }
        },

        forceAdvanceTask: (taskId, targetStage) => {
          try {
            stageProgressionService.forceAdvanceToStage(taskId, { getState: get }, targetStage);
            return true;
          } catch (error) {
            set({ error: `Force advance failed: ${error.message}` }, false, 'forceAdvanceTaskError');
            return false;
          }
        },

        getTaskProgressionStatus: (taskId) => {
          return stageProgressionService.getProgressionStatus(taskId);
        },

        getAllActiveProgressions: () => {
          return stageProgressionService.getActiveProgressions();
        },

        // Data export/import
        exportData: () => {
          const state = get();
          const exportData = {
            selectedProject: state.selectedProject,
            availableProjects: state.availableProjects,
            tasks: state.tasks,
            taskIdCounter: state.taskIdCounter,
            exportedAt: new Date().toISOString(),
            version: '1.0.0',
          };

          return localStorageService.setItem('backup', exportData) ? exportData : null;
        },

        importData: (importData) => {
          try {
            if (!importData || typeof importData !== 'object') {
              throw new Error('Invalid import data format');
            }

            set({
              selectedProject: importData.selectedProject || null,
              availableProjects: importData.availableProjects || [],
              tasks: importData.tasks || [],
              taskIdCounter: importData.taskIdCounter || 1,
            }, false, 'importData');

            return true;
          } catch (error) {
            set({ error: `Import failed: ${error.message}` }, false, 'importDataError');
            return false;
          }
        },

        // Storage management
        getStorageInfo: () => {
          return localStorageService.getStorageInfo();
        },

        clearAllData: () => {
          const success = localStorageService.clear();
          if (success) {
            set(initialState, false, 'clearAllData');
          }
          return success;
        },

        // Task filtering and search
        searchTasks: (query) => {
          const { tasks } = get();
          if (!query) return tasks;

          const lowercaseQuery = query.toLowerCase();
          return tasks.filter(task =>
            task.title.toLowerCase().includes(lowercaseQuery) ||
            task.description.toLowerCase().includes(lowercaseQuery) ||
            task.stage.toLowerCase().includes(lowercaseQuery) ||
            task.substage.toLowerCase().includes(lowercaseQuery)
          );
        },

        getTasksByPipeline: (pipelineId) => {
          const { tasks } = get();
          return tasks.filter(task => task.pipelineId === pipelineId);
        },

        getTasksByDateRange: (startDate, endDate) => {
          const { tasks } = get();
          return tasks.filter(task => {
            const taskDate = new Date(task.createdAt);
            return taskDate >= startDate && taskDate <= endDate;
          });
        },

        // Statistics
        getStatistics: () => {
          const { tasks } = get();

          const stats = {
            totalTasks: tasks.length,
            byStage: {},
            byPipeline: {},
            completedTasks: 0,
            inProgressTasks: 0,
            erroredTasks: 0,
            averageProgress: 0,
          };

          // Calculate statistics
          let totalProgress = 0;

          tasks.forEach(task => {
            // By stage
            stats.byStage[task.stage] = (stats.byStage[task.stage] || 0) + 1;

            // By pipeline
            stats.byPipeline[task.pipelineId] = (stats.byPipeline[task.pipelineId] || 0) + 1;

            // Status counts
            if (task.stage === 'errored') {
              stats.erroredTasks++;
            } else if (task.stage === 'pr' && task.progress === 100) {
              stats.completedTasks++;
            } else {
              stats.inProgressTasks++;
            }

            totalProgress += task.progress || 0;
          });

          stats.averageProgress = tasks.length > 0 ? Math.round(totalProgress / tasks.length) : 0;

          return stats;
        },

        // Reset store
        reset: () => {
          set(initialState, false, 'reset');
        },
      }),
      {
        name: 'agentic-kanban-storage',
        version: 1,
        partialize: (state) => ({
          // Don't persist selectedProject as it contains non-serializable FileSystemDirectoryHandle
          availableProjects: state.availableProjects.map(project => ({
            ...project,
            handle: undefined // Remove non-serializable handle
          })),
          tasks: state.tasks,
          taskIdCounter: state.taskIdCounter,
        }),
      }
    ),
    {
      name: 'AgenticKanban',
    }
  )
);

export default useKanbanStore;