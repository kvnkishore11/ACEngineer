import { useState, useEffect } from 'react';
import { useKanbanStore } from '../stores/kanbanStore';
import { Folder, FolderOpen, CheckCircle, XCircle, Plus, FileText } from 'lucide-react';

const ProjectSelector = () => {
  const {
    availableProjects,
    selectProject: selectProjectInStore,
    addProject,
    setError,
    setLoading,
  } = useKanbanStore();

  const [showNewProject, setShowNewProject] = useState(false);
  const [validationStatus, setValidationStatus] = useState(null);
  const [isSelectingFolder, setIsSelectingFolder] = useState(false);

  // Check if File System Access API is supported
  const isFileSystemAPISupported = 'showDirectoryPicker' in window;

  // Project selection using File System Access API
  const selectProjectFromFileSystem = async () => {
    try {
      if (!isFileSystemAPISupported) {
        setError('File System Access API is not supported in this browser. Please use Chrome, Edge, or another compatible browser.');
        return;
      }

      setIsSelectingFolder(true);
      const projectHandle = await window.showDirectoryPicker();

      // Validate project structure
      const validation = await validateProjectStructure(projectHandle);

      if (!validation.isValid) {
        setError('Selected project is missing required structure (agentics/ or .claude/ directories)');
        return;
      }

      // Create project object
      const project = {
        id: `project-${Date.now()}`,
        name: projectHandle.name,
        path: projectHandle.name, // We can't get full path from File API for security
        handle: projectHandle, // Store the handle for file operations
        isValid: validation.isValid,
        hasAgentics: validation.hasAgentics,
        hasClaude: validation.hasClaude,
        description: 'Selected project with ADW support',
        lastModified: new Date().toISOString(),
      };

      addProject(project);
      selectProjectInStore(project);

    } catch (error) {
      if (error.name !== 'AbortError') {
        setError(`Failed to select project: ${error.message}`);
      }
    } finally {
      setIsSelectingFolder(false);
    }
  };

  // Validate project has required folders
  const validateProjectStructure = async (projectHandle) => {
    try {
      let hasAgentics = false;
      let hasClaude = false;

      try {
        await projectHandle.getDirectoryHandle('agentics');
        hasAgentics = true;
      } catch {
        // agentics folder not found
      }

      try {
        await projectHandle.getDirectoryHandle('.claude');
        hasClaude = true;
      } catch {
        // .claude folder not found
      }

      return {
        isValid: hasAgentics && hasClaude,
        hasAgentics,
        hasClaude,
      };
    } catch (error) {
      console.error('Error validating project structure:', error);
      return {
        isValid: false,
        hasAgentics: false,
        hasClaude: false,
      };
    }
  };

  const handleSelectProject = (project) => {
    if (!project.isValid) {
      setError('Selected project is missing required structure (agentics/ or .claude/ directories)');
      return;
    }

    selectProjectInStore(project);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <FolderOpen className="h-16 w-16 text-primary-600 mx-auto mb-4" />
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Select a Project
        </h1>
        <p className="text-lg text-gray-600">
          Choose a project with ADW support (agentics/ and .claude/ directories)
        </p>
      </div>

      {/* Recent Projects */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Projects</h2>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {availableProjects.map((project) => (
            <div
              key={project.id}
              className={`card cursor-pointer transition-all hover:shadow-md ${
                project.isValid
                  ? 'hover:border-primary-300'
                  : 'opacity-75 hover:border-red-300'
              }`}
              onClick={() => handleSelectProject(project)}
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center space-x-2">
                  <Folder className={`h-5 w-5 ${
                    project.isValid ? 'text-primary-600' : 'text-gray-400'
                  }`} />
                  <h3 className="font-medium text-gray-900">{project.name}</h3>
                </div>
                {project.isValid ? (
                  <CheckCircle className="h-5 w-5 text-green-500" />
                ) : (
                  <XCircle className="h-5 w-5 text-red-500" />
                )}
              </div>

              <p className="text-sm text-gray-600 mb-3">{project.description}</p>

              <div className="space-y-2">
                <div className="text-xs text-gray-500">
                  {project.path}
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex space-x-3">
                    <div className={`flex items-center space-x-1 ${
                      project.hasAgentics ? 'text-green-600' : 'text-red-600'
                    }`}>
                      <div className={`h-2 w-2 rounded-full ${
                        project.hasAgentics ? 'bg-green-500' : 'bg-red-500'
                      }`}></div>
                      <span className="text-xs">agentics/</span>
                    </div>

                    <div className={`flex items-center space-x-1 ${
                      project.hasClaude ? 'text-green-600' : 'text-red-600'
                    }`}>
                      <div className={`h-2 w-2 rounded-full ${
                        project.hasClaude ? 'bg-green-500' : 'bg-red-500'
                      }`}></div>
                      <span className="text-xs">.claude/</span>
                    </div>
                  </div>

                  <span className="text-xs text-gray-500">
                    {formatDate(project.lastModified)}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Select New Project */}
      <div className="border-t border-gray-200 pt-8">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Select Project</h2>

          {isFileSystemAPISupported ? (
            <button
              onClick={selectProjectFromFileSystem}
              disabled={isSelectingFolder}
              className="btn-primary flex items-center space-x-2 mx-auto"
            >
              <Folder className="h-4 w-4" />
              <span>{isSelectingFolder ? 'Selecting...' : 'Browse Folders'}</span>
            </button>
          ) : (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 max-w-2xl mx-auto">
              <div className="flex items-center space-x-2 mb-2">
                <XCircle className="h-5 w-5 text-yellow-600" />
                <span className="font-medium text-yellow-800">
                  File System Access Not Supported
                </span>
              </div>
              <p className="text-sm text-yellow-700">
                Your browser doesn't support the File System Access API. Please use Chrome, Edge, or another compatible browser for the best experience.
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Help Section */}
      <div className="mt-12 bg-blue-50 rounded-lg p-6">
        <div className="flex items-start space-x-3">
          <FileText className="h-6 w-6 text-blue-600 mt-1" />
          <div>
            <h3 className="font-medium text-blue-900 mb-2">
              Project Requirements
            </h3>
            <div className="text-sm text-blue-800 space-y-1">
              <p>• <strong>agentics/</strong> directory with ADW pipeline configurations</p>
              <p>• <strong>.claude/</strong> directory with command primitives</p>
              <p>• Valid project structure for AI-driven development workflows</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectSelector;