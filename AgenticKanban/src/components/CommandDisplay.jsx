import { useState } from 'react';
import { Copy, Check, Terminal, Settings, ToggleLeft, ToggleRight } from 'lucide-react';
import ExecutionStatus from './ExecutionStatus';
import { useKanbanStore } from '../stores/kanbanStore';

const CommandDisplay = ({ command, taskData, onClose, executionMode = 'manual', isExecuting = false, executionError = null }) => {
  const [copied, setCopied] = useState(false);
  const [showSettings, setShowSettings] = useState(false);

  const {
    getExecutionConfig,
    updateExecutionConfig,
    selectedProject,
    isTaskExecuting
  } = useKanbanStore();

  const executionConfig = getExecutionConfig();

  // Check if this task is currently executing
  const adwId = taskData?.adw_id;
  const taskExecuting = adwId ? isTaskExecuting(adwId) : false;

  // Show execution status if we're in execution mode or if task is executing
  if (executionMode === 'automatic' || isExecuting || taskExecuting) {
    return (
      <ExecutionStatus
        taskData={taskData}
        adwId={adwId}
        projectHandle={selectedProject?.handle}
        onClose={onClose}
        isExecuting={isExecuting || taskExecuting}
        executionError={executionError}
      />
    );
  }

  const handleCopyCommand = async () => {
    try {
      await navigator.clipboard.writeText(command.full);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error('Failed to copy command:', error);
    }
  };

  const handleToggleAutoExecution = () => {
    updateExecutionConfig({
      autoExecute: !executionConfig.autoExecute
    });
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[80vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <Terminal className="h-6 w-6 text-primary-600" />
            <h3 className="text-lg font-semibold text-gray-900">
              Manual Workflow Execution
            </h3>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setShowSettings(!showSettings)}
              className="text-gray-400 hover:text-gray-600 p-1 rounded"
              title="Settings"
            >
              <Settings className="h-5 w-5" />
            </button>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600"
            >
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <div className="space-y-4">
          <div>
            <p className="text-sm text-gray-600 mb-2">
              Task: <span className="font-medium">{taskData.title}</span>
            </p>
            <p className="text-sm text-gray-600 mb-4">
              ADW ID: <span className="font-mono font-medium">{taskData.adw_id}</span>
            </p>
          </div>

          {/* Settings Panel */}
          {showSettings && (
            <div className="bg-gray-50 rounded-lg p-4 border">
              <h4 className="font-medium text-gray-900 mb-3">Execution Settings</h4>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div>
                    <span className="text-sm font-medium text-gray-700">Automatic Execution</span>
                    <p className="text-xs text-gray-500">Execute workflows automatically without manual commands</p>
                  </div>
                  <button
                    onClick={handleToggleAutoExecution}
                    className="flex-shrink-0"
                    title={`Turn ${executionConfig.autoExecute ? 'off' : 'on'} automatic execution`}
                  >
                    {executionConfig.autoExecute ? (
                      <ToggleRight className="h-6 w-6 text-blue-600" />
                    ) : (
                      <ToggleLeft className="h-6 w-6 text-gray-400" />
                    )}
                  </button>
                </div>
                <div className="text-xs text-gray-600 bg-white p-2 rounded border">
                  <strong>Note:</strong> When enabled, new tasks will execute automatically without showing this modal.
                  Manual execution will still be available as a fallback if automatic execution fails.
                </div>
              </div>
            </div>
          )}

          {/* Warning about manual execution */}
          <div className="bg-yellow-50 rounded-lg p-4">
            <h4 className="font-medium text-yellow-900 mb-2">Manual Execution Required</h4>
            <p className="text-sm text-yellow-800">
              Automatic execution is not available for this task. This may be because:
            </p>
            <ul className="text-sm text-yellow-800 mt-2 list-disc list-inside">
              <li>Automatic execution is disabled in settings</li>
              <li>The project structure doesn't support automatic execution</li>
              <li>File system access permissions are restricted</li>
            </ul>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Run this command in your terminal:
            </label>
            <div className="relative">
              <code className="block bg-gray-900 text-green-400 p-4 rounded-lg text-sm overflow-x-auto">
                {command.full}
              </code>
              <button
                onClick={handleCopyCommand}
                className={`absolute top-2 right-2 p-2 rounded ${
                  copied
                    ? 'bg-green-600 text-white'
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
                title={copied ? 'Copied!' : 'Copy command'}
              >
                {copied ? (
                  <Check className="h-4 w-4" />
                ) : (
                  <Copy className="h-4 w-4" />
                )}
              </button>
            </div>
          </div>

          <div className="bg-blue-50 rounded-lg p-4">
            <h4 className="font-medium text-blue-900 mb-2">Instructions:</h4>
            <ol className="text-sm text-blue-800 space-y-1">
              <li>1. Copy the command above</li>
              <li>2. Open a terminal in your project directory</li>
              <li>3. Paste and run the command</li>
              <li>4. The Kanban board will automatically update as the workflow progresses</li>
            </ol>
          </div>

          <div className="bg-yellow-50 rounded-lg p-4">
            <h4 className="font-medium text-yellow-900 mb-2">Note:</h4>
            <p className="text-sm text-yellow-800">
              The Python orchestrator script will create state files that this Kanban board monitors.
              You can track progress in real-time as the workflow executes.
            </p>
          </div>
        </div>

        <div className="flex justify-end mt-6">
          <button
            onClick={onClose}
            className="btn-secondary"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default CommandDisplay;