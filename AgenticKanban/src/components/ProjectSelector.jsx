import { useState, useEffect } from 'react';
import { useKanbanStore } from '../stores/kanbanStore';
import { Folder, FolderOpen, CheckCircle, XCircle, Plus, FileText } from 'lucide-react';

const ProjectSelector = () => {
  const {
    availableProjects,
    selectProject,
    addProject,
    setError,
    setLoading,
  } = useKanbanStore();

  const [showNewProject, setShowNewProject] = useState(false);
  const [newProjectPath, setNewProjectPath] = useState('');
  const [validationStatus, setValidationStatus] = useState(null);

  // Simulated project discovery for demo purposes
  const simulatedProjects = [
    {
      id: 'example-project-1',
      name: 'AgenticKanban',
      path: '/Users/kvnkishore/WebstormProjects/AgenticEngineer/AgenticKanban',
      isValid: true,
      hasAgentics: true,
      hasClaude: true,
      description: 'AI-Driven Development Workflow Kanban Board',
      lastModified: new Date().toISOString(),
    },
    {
      id: 'example-project-2',
      name: 'React Dashboard',
      path: '/Users/demo/projects/react-dashboard',
      isValid: true,
      hasAgentics: true,
      hasClaude: true,
      description: 'Analytics Dashboard with ADW support',
      lastModified: new Date(Date.now() - 86400000).toISOString(), // 1 day ago
    },
    {
      id: 'example-project-3',
      name: 'Node API',
      path: '/Users/demo/projects/node-api',
      isValid: false,
      hasAgentics: false,
      hasClaude: true,
      description: 'REST API (missing agentics folder)',
      lastModified: new Date(Date.now() - 172800000).toISOString(), // 2 days ago
    },
  ];

  useEffect(() => {
    // Initialize with simulated projects if none exist
    if (availableProjects.length === 0) {
      simulatedProjects.forEach(project => {
        addProject(project);
      });
    }
  }, [availableProjects.length, addProject]);

  const validateProject = (path) => {
    // Simulate project validation
    setLoading(true);

    setTimeout(() => {
      const isValid = Math.random() > 0.3; // 70% chance of being valid
      const hasAgentics = Math.random() > 0.2; // 80% chance of having agentics
      const hasClaude = Math.random() > 0.1; // 90% chance of having .claude

      setValidationStatus({
        isValid: isValid && hasAgentics && hasClaude,
        hasAgentics,
        hasClaude,
        path,
      });

      setLoading(false);
    }, 1000);
  };

  const handleSelectProject = (project) => {
    if (!project.isValid) {
      setError('Selected project is missing required structure (agentics/ or .claude/ directories)');
      return;
    }

    selectProject(project);
  };

  const handleAddNewProject = () => {
    if (!newProjectPath.trim()) {
      setError('Please enter a valid project path');
      return;
    }

    if (validationStatus && validationStatus.isValid) {
      const newProject = {
        id: `project-${Date.now()}`,
        name: newProjectPath.split('/').pop() || 'New Project',
        path: newProjectPath,
        isValid: true,
        hasAgentics: validationStatus.hasAgentics,
        hasClaude: validationStatus.hasClaude,
        description: 'Recently added project',
        lastModified: new Date().toISOString(),
      };

      addProject(newProject);
      selectProject(newProject);
    } else {
      setError('Please validate the project first');
    }
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

      {/* Add New Project */}
      <div className="border-t border-gray-200 pt-8">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-gray-900">Add New Project</h2>
          <button
            onClick={() => setShowNewProject(!showNewProject)}
            className="btn-secondary flex items-center space-x-2"
          >
            <Plus className="h-4 w-4" />
            <span>Browse</span>
          </button>
        </div>

        {showNewProject && (
          <div className="card max-w-2xl">
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Project Path
                </label>
                <input
                  type="text"
                  value={newProjectPath}
                  onChange={(e) => setNewProjectPath(e.target.value)}
                  placeholder="/path/to/your/project"
                  className="input-field"
                />
                <p className="mt-1 text-xs text-gray-500">
                  Enter the full path to your project directory
                </p>
              </div>

              <div className="flex space-x-3">
                <button
                  onClick={() => validateProject(newProjectPath)}
                  className="btn-secondary"
                  disabled={!newProjectPath.trim()}
                >
                  Validate Project
                </button>

                {validationStatus && (
                  <button
                    onClick={handleAddNewProject}
                    className="btn-primary"
                    disabled={!validationStatus.isValid}
                  >
                    Add Project
                  </button>
                )}
              </div>

              {validationStatus && (
                <div className={`p-4 rounded-md ${
                  validationStatus.isValid
                    ? 'bg-green-50 border border-green-200'
                    : 'bg-red-50 border border-red-200'
                }`}>
                  <div className="flex items-center space-x-2 mb-2">
                    {validationStatus.isValid ? (
                      <CheckCircle className="h-5 w-5 text-green-500" />
                    ) : (
                      <XCircle className="h-5 w-5 text-red-500" />
                    )}
                    <span className={`font-medium ${
                      validationStatus.isValid ? 'text-green-800' : 'text-red-800'
                    }`}>
                      {validationStatus.isValid
                        ? 'Project is valid for ADW workflows'
                        : 'Project validation failed'
                      }
                    </span>
                  </div>

                  <div className="space-y-1 text-sm">
                    <div className={`flex items-center space-x-2 ${
                      validationStatus.hasAgentics ? 'text-green-700' : 'text-red-700'
                    }`}>
                      <div className={`h-2 w-2 rounded-full ${
                        validationStatus.hasAgentics ? 'bg-green-500' : 'bg-red-500'
                      }`}></div>
                      <span>
                        agentics/ directory {validationStatus.hasAgentics ? 'found' : 'missing'}
                      </span>
                    </div>

                    <div className={`flex items-center space-x-2 ${
                      validationStatus.hasClaude ? 'text-green-700' : 'text-red-700'
                    }`}>
                      <div className={`h-2 w-2 rounded-full ${
                        validationStatus.hasClaude ? 'bg-green-500' : 'bg-red-500'
                      }`}></div>
                      <span>
                        .claude/ directory {validationStatus.hasClaude ? 'found' : 'missing'}
                      </span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
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