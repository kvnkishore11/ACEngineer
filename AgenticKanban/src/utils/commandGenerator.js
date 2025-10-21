// Command generation utilities for the simplified workflow

/**
 * Generate a unique ADW ID for a task
 */
export const generateAdwId = () => {
  return `adw_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
};

/**
 * Generate execution command for user
 */
export const generateWorkflowCommand = (taskData, projectHandle) => {
  const projectPath = projectHandle ? projectHandle.name : 'your-project';

  const command = {
    directory: `cd ${projectPath}/agentics/adws`,
    execution: `python adw_orchestrator.py '${JSON.stringify(taskData)}'`,
    full: `cd ${projectPath}/agentics/adws && python adw_orchestrator.py '${JSON.stringify(taskData)}'`
  };

  return command;
};

/**
 * Create task data object for ADW workflow
 */
export const createTaskData = (taskInput, adwId) => {
  return {
    adw_id: adwId,
    title: taskInput.title,
    description: taskInput.description,
    type: taskInput.type || 'feature',
    priority: taskInput.priority || 'medium',
    stages: taskInput.stages || ['plan', 'build', 'test', 'review'],
    created_at: new Date().toISOString(),
    project_context: {
      // Add any project-specific context here
    }
  };
};

/**
 * Poll workflow state from file system
 */
export const pollWorkflowState = (adwId, projectHandle, onStateUpdate) => {
  const pollInterval = setInterval(async () => {
    try {
      // Get the agentics directory
      const agenticsDir = await projectHandle.getDirectoryHandle('agentics');
      const agentsDir = await agenticsDir.getDirectoryHandle('agents');
      const adwDir = await agentsDir.getDirectoryHandle(adwId);

      // Read the state file
      const stateFile = await adwDir.getFileHandle('adw_state.json');
      const file = await stateFile.getFile();
      const content = await file.text();
      const state = JSON.parse(content);

      // Update the task state
      onStateUpdate(adwId, state);

      // Stop polling if workflow completed
      if (state.overall_status === 'completed' || state.overall_status === 'failed') {
        clearInterval(pollInterval);
      }
    } catch (error) {
      // File doesn't exist yet or access error
      console.log('Waiting for state file...', error.message);
    }
  }, 2000); // Poll every 2 seconds

  return pollInterval;
};

/**
 * Update task from ADW state
 */
export const updateTaskFromState = (state) => {
  const task = {
    stage: mapStateToStage(state.current_stage),
    status: state.overall_status,
    progress: calculateProgress(state),
    logs: state.logs || [],
    lastUpdated: new Date().toISOString(),
    details: {
      current_stage: state.current_stage,
      completed_stages: state.completed_stages || [],
      failed_stages: state.failed_stages || [],
      current_action: state.current_action,
      metrics: state.metrics || {}
    }
  };

  return task;
};

/**
 * Map ADW state to Kanban stage
 */
const mapStateToStage = (adwStage) => {
  const stageMapping = {
    'planning': 'plan',
    'plan': 'plan',
    'implementation': 'build',
    'build': 'build',
    'building': 'build',
    'testing': 'test',
    'test': 'test',
    'review': 'review',
    'reviewing': 'review',
    'pr': 'pr',
    'pull_request': 'pr',
    'completed': 'pr'
  };

  return stageMapping[adwStage?.toLowerCase()] || 'backlog';
};

/**
 * Calculate progress percentage from state
 */
const calculateProgress = (state) => {
  if (!state.completed_stages || !state.total_stages) {
    return 0;
  }

  return Math.round((state.completed_stages.length / state.total_stages) * 100);
};