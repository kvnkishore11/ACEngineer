// Workflow execution utility for automatic ADW command execution
// Optimized for the new ADWS (Agentic Development Workflow System)
// Uses File System Access API to create trigger files for the Python orchestrator

/**
 * Execute ADW workflow automatically by writing task files
 * @param {Object} taskData - Task data object
 * @param {FileSystemDirectoryHandle} projectHandle - Project directory handle
 * @returns {Promise<Object>} Execution result
 */
export const executeWorkflow = async (taskData, projectHandle) => {
  try {
    // Validate inputs
    if (!taskData || !taskData.adw_id) {
      throw new Error('Task data with adw_id is required');
    }

    if (!projectHandle) {
      throw new Error('Project directory handle is required');
    }

    // Get or create agentics directory structure
    const agenticsDir = await getOrCreateDirectory(projectHandle, 'agentics');
    const adwsDir = await getOrCreateDirectory(agenticsDir, 'adws');
    const agentsDir = await getOrCreateDirectory(agenticsDir, 'agents');

    // Create task-specific directory
    const taskDir = await getOrCreateDirectory(agentsDir, taskData.adw_id);

    // Write task data file with enhanced metadata
    await writeTaskDataFile(taskDir, taskData);

    // Create execution trigger file for ADWS orchestrator
    await createTriggerFile(adwsDir, taskData);

    // Return success result
    return {
      success: true,
      adwId: taskData.adw_id,
      message: 'Workflow execution initiated automatically',
      triggerCreated: true,
      taskDataWritten: true
    };

  } catch (error) {
    console.error('Workflow execution failed:', error);
    return {
      success: false,
      error: error.message,
      adwId: taskData.adw_id
    };
  }
};

/**
 * Get or create a directory handle
 * @param {FileSystemDirectoryHandle} parentDir - Parent directory
 * @param {string} dirName - Directory name to get or create
 * @returns {Promise<FileSystemDirectoryHandle>}
 */
const getOrCreateDirectory = async (parentDir, dirName) => {
  try {
    return await parentDir.getDirectoryHandle(dirName);
  } catch (error) {
    if (error.name === 'NotFoundError') {
      return await parentDir.getDirectoryHandle(dirName, { create: true });
    }
    throw error;
  }
};

/**
 * Write task data to file for Python orchestrator
 * @param {FileSystemDirectoryHandle} taskDir - Task directory
 * @param {Object} taskData - Task data object
 */
const writeTaskDataFile = async (taskDir, taskData) => {
  // Use state.json following TAC-7 convention
  const fileHandle = await taskDir.getFileHandle('state.json', { create: true });
  const writable = await fileHandle.createWritable();

  const taskDataWithMetadata = {
    ...taskData,
    execution_mode: 'automatic',
    triggered_at: new Date().toISOString(),
    kanban_integration: true,
    trigger_source: 'kanban_ui',
    workflow_status: 'initialized',
    ui_metadata: {
      browser: navigator.userAgent,
      timestamp: new Date().toISOString(),
      session_id: Date.now().toString(36)
    }
  };

  await writable.write(JSON.stringify(taskDataWithMetadata, null, 2));
  await writable.close();
};

/**
 * Create trigger file for Python orchestrator to detect
 * @param {FileSystemDirectoryHandle} adwsDir - ADWs directory
 * @param {Object} taskData - Task data object
 */
const createTriggerFile = async (adwsDir, taskData) => {
  const triggerFileName = `trigger_${taskData.adw_id}.json`;
  const fileHandle = await adwsDir.getFileHandle(triggerFileName, { create: true });
  const writable = await fileHandle.createWritable();

  const triggerData = {
    adw_id: taskData.adw_id,
    action: 'execute',
    task_file: `../agents/${taskData.adw_id}/state.json`,
    created_at: new Date().toISOString(),
    status: 'pending'
  };

  await writable.write(JSON.stringify(triggerData, null, 2));
  await writable.close();
};

/**
 * Check if automatic execution is supported
 * @param {FileSystemDirectoryHandle} projectHandle - Project directory handle
 * @returns {Promise<boolean>}
 */
export const isAutoExecutionSupported = async (projectHandle) => {
  try {
    if (!projectHandle) return false;

    // Check if we can access agentics directory
    const agenticsDir = await projectHandle.getDirectoryHandle('agentics');

    // Check if adws directory exists
    await agenticsDir.getDirectoryHandle('adws');

    return true;
  } catch (error) {
    console.warn('Auto-execution not supported:', error.message);
    return false;
  }
};

/**
 * Get execution status for a task
 * @param {string} adwId - ADW ID
 * @param {FileSystemDirectoryHandle} projectHandle - Project directory handle
 * @returns {Promise<Object>} Status object
 */
export const getExecutionStatus = async (adwId, projectHandle) => {
  try {
    const agenticsDir = await projectHandle.getDirectoryHandle('agentics');
    const agentsDir = await agenticsDir.getDirectoryHandle('agents');
    const taskDir = await agentsDir.getDirectoryHandle(adwId);

    // Try to read state file (TAC-7 convention)
    try {
      const stateFile = await taskDir.getFileHandle('state.json');
      const file = await stateFile.getFile();
      const content = await file.text();
      const state = JSON.parse(content);

      return {
        found: true,
        state,
        status: state.overall_status || 'unknown'
      };
    } catch {
      // State file doesn't exist yet
      return {
        found: false,
        status: 'initializing',
        message: 'Waiting for execution to begin...'
      };
    }
  } catch (error) {
    return {
      found: false,
      status: 'error',
      error: error.message
    };
  }
};

/**
 * Clean up execution files after completion
 * @param {string} adwId - ADW ID
 * @param {FileSystemDirectoryHandle} projectHandle - Project directory handle
 */
export const cleanupExecution = async (adwId, projectHandle) => {
  try {
    const agenticsDir = await projectHandle.getDirectoryHandle('agentics');
    const adwsDir = await agenticsDir.getDirectoryHandle('adws');

    // Remove trigger file
    const triggerFileName = `trigger_${adwId}.json`;
    try {
      await adwsDir.removeEntry(triggerFileName);
    } catch {
      // File might not exist, that's okay
      console.log('Trigger file already removed or not found');
    }
  } catch (error) {
    console.warn('Cleanup failed:', error.message);
  }
};

/**
 * Force stop execution for a task
 * @param {string} adwId - ADW ID
 * @param {FileSystemDirectoryHandle} projectHandle - Project directory handle
 */
export const stopExecution = async (adwId, projectHandle) => {
  try {
    const agenticsDir = await projectHandle.getDirectoryHandle('agentics');
    const agentsDir = await agenticsDir.getDirectoryHandle('agents');
    const taskDir = await agentsDir.getDirectoryHandle(adwId);

    // Create stop signal file
    const stopFile = await taskDir.getFileHandle('stop_signal.txt', { create: true });
    const writable = await stopFile.createWritable();
    await writable.write(`STOP_REQUESTED_AT_${new Date().toISOString()}`);
    await writable.close();

    return { success: true, message: 'Stop signal sent' };
  } catch (error) {
    return { success: false, error: error.message };
  }
};

/**
 * Get configuration for automatic execution
 * @returns {Object} Configuration object
 */
export const getExecutionConfig = () => {
  const config = localStorage.getItem('adw_execution_config');
  if (config) {
    try {
      return JSON.parse(config);
    } catch {
      console.warn('Invalid execution config, using defaults');
    }
  }

  // Default configuration
  return {
    autoExecute: true,
    fallbackToManual: true,
    cleanupAfterCompletion: true,
    pollingInterval: 2000
  };
};

/**
 * Save execution configuration
 * @param {Object} config - Configuration object
 */
export const saveExecutionConfig = (config) => {
  try {
    localStorage.setItem('adw_execution_config', JSON.stringify(config));
    return true;
  } catch (error) {
    console.error('Failed to save execution config:', error);
    return false;
  }
};

export default {
  executeWorkflow,
  isAutoExecutionSupported,
  getExecutionStatus,
  cleanupExecution,
  stopExecution,
  getExecutionConfig,
  saveExecutionConfig
};