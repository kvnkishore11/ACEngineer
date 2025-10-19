import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import adwService from '../services/adwService';
import localStorageService from '../services/localStorage';
import stageProgressionService from '../services/stageProgressionService';

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
          const { tasks, stages } = get();

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
          selectedProject: state.selectedProject,
          availableProjects: state.availableProjects,
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