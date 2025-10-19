import { useState } from 'react';
import { useKanbanStore, WORK_ITEM_TYPES, QUEUEABLE_STAGES } from '../stores/kanbanStore';
import { X, Plus, Upload, Bold, Italic, Underline, Image as ImageIcon } from 'lucide-react';
import { useDropzone } from 'react-dropzone';
import MDEditor from '@uiw/react-md-editor';

const TaskInput = () => {
  const {
    createTask,
    toggleTaskInput,
    validateTask,
  } = useKanbanStore();

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [workItemType, setWorkItemType] = useState(WORK_ITEM_TYPES.FEATURE);
  const [queuedStages, setQueuedStages] = useState(['plan', 'implement']);
  const [images, setImages] = useState([]);
  const [errors, setErrors] = useState([]);

  // Image upload with react-dropzone
  const onDrop = (acceptedFiles) => {
    const newImages = acceptedFiles.map(file => ({
      id: Date.now() + Math.random(),
      file,
      url: URL.createObjectURL(file),
      name: file.name,
      size: file.size,
    }));
    setImages(prev => [...prev, ...newImages]);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.webp'],
    },
    maxSize: 5 * 1024 * 1024, // 5MB
  });

  const removeImage = (imageId) => {
    setImages(prev => {
      const updated = prev.filter(img => img.id !== imageId);
      // Clean up object URLs
      const removed = prev.find(img => img.id === imageId);
      if (removed) {
        URL.revokeObjectURL(removed.url);
      }
      return updated;
    });
  };

  const handleStageToggle = (stageId) => {
    setQueuedStages(prev => {
      if (prev.includes(stageId)) {
        return prev.filter(id => id !== stageId);
      } else {
        return [...prev, stageId];
      }
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const taskData = {
      title: title.trim(),
      description: description.trim(),
      workItemType,
      queuedStages,
      images,
    };

    const validation = validateTask(taskData);

    if (!validation.isValid) {
      setErrors(validation.errors);
      return;
    }

    createTask(taskData);

    // Reset form
    setTitle('');
    setDescription('');
    setWorkItemType(WORK_ITEM_TYPES.FEATURE);
    setQueuedStages(['plan', 'implement']);
    setImages([]);
    setErrors([]);
  };

  const workItemTypeOptions = [
    { value: WORK_ITEM_TYPES.FEATURE, label: 'Feature', color: 'bg-blue-100 text-blue-800' },
    { value: WORK_ITEM_TYPES.CHORE, label: 'Chore', color: 'bg-gray-100 text-gray-800' },
    { value: WORK_ITEM_TYPES.BUG, label: 'Bug', color: 'bg-red-100 text-red-800' },
    { value: WORK_ITEM_TYPES.PATCH, label: 'Patch', color: 'bg-yellow-100 text-yellow-800' },
  ];

  return (
    <div className="modal-overlay fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="modal-content bg-white rounded-lg shadow-xl max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">Create New Task</h2>
          <button
            onClick={toggleTaskInput}
            className="p-2 text-gray-400 hover:text-gray-600"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* Error Messages */}
          {errors.length > 0 && (
            <div className="bg-red-50 border border-red-200 rounded-md p-4">
              <h3 className="text-sm font-medium text-red-800 mb-2">Please fix the following errors:</h3>
              <ul className="list-disc list-inside text-sm text-red-700 space-y-1">
                {errors.map((error, index) => (
                  <li key={index}>{error}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Optional Title Field */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Task Title (optional)
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Enter task title (optional)..."
              className="input-field"
            />
            <p className="mt-1 text-xs text-gray-500">
              Leave empty to auto-generate from description
            </p>
          </div>

          {/* Work Item Type Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Work Item Type *
            </label>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {workItemTypeOptions.map((option) => (
                <label
                  key={option.value}
                  className={`relative cursor-pointer rounded-lg border p-4 text-center transition-all
                    ${workItemType === option.value
                      ? 'border-blue-600 bg-blue-50 ring-2 ring-blue-600'
                      : 'border-gray-200 hover:border-gray-300'
                    }`}
                >
                  <input
                    type="radio"
                    name="workItemType"
                    value={option.value}
                    checked={workItemType === option.value}
                    onChange={(e) => setWorkItemType(e.target.value)}
                    className="sr-only"
                  />
                  <div className={`inline-flex items-center justify-center w-full px-3 py-1 rounded-full text-sm font-medium ${option.color}`}>
                    {option.label}
                  </div>
                </label>
              ))}
            </div>
          </div>

          {/* Stage Queue Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Queue Stages *
            </label>
            <p className="text-sm text-gray-500 mb-3">
              Select the stages this task should progress through
            </p>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {QUEUEABLE_STAGES.map((stage) => (
                <label
                  key={stage.id}
                  className={`relative cursor-pointer rounded-lg border p-3 transition-all
                    ${queuedStages.includes(stage.id)
                      ? 'border-blue-600 bg-blue-50 ring-2 ring-blue-600'
                      : 'border-gray-200 hover:border-gray-300'
                    }`}
                >
                  <input
                    type="checkbox"
                    checked={queuedStages.includes(stage.id)}
                    onChange={() => handleStageToggle(stage.id)}
                    className="sr-only"
                  />
                  <div className="flex items-center">
                    <div className={`w-3 h-3 rounded-full mr-2 bg-${stage.color}-400`}></div>
                    <span className="text-sm font-medium">{stage.name}</span>
                  </div>
                </label>
              ))}
            </div>
          </div>

          {/* Rich Text Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Description *
            </label>
            <div className="border border-gray-300 rounded-md overflow-hidden">
              <MDEditor
                value={description}
                onChange={setDescription}
                preview="edit"
                hideToolbar={false}
                visibleDragBar={false}
                textareaProps={{
                  placeholder: 'Describe what needs to be done... (Supports Markdown formatting)',
                  style: { fontSize: 14, lineHeight: 1.5 }
                }}
                height={150}
              />
            </div>
            <p className="mt-1 text-xs text-gray-500">
              Use Markdown for formatting (bold, italic, lists, links, etc.)
            </p>
          </div>

          {/* Image Upload */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Attachments
            </label>

            {/* Dropzone */}
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors
                ${isDragActive
                  ? 'border-blue-400 bg-blue-50'
                  : 'border-gray-300 hover:border-gray-400'
                }`}
            >
              <input {...getInputProps()} />
              <ImageIcon className="h-8 w-8 text-gray-400 mx-auto mb-2" />
              {isDragActive ? (
                <p className="text-blue-600">Drop images here...</p>
              ) : (
                <div>
                  <p className="text-gray-600">Drag & drop images here, or click to select</p>
                  <p className="text-xs text-gray-500 mt-1">Supports PNG, JPG, GIF, WebP (max 5MB)</p>
                </div>
              )}
            </div>

            {/* Uploaded Images Preview */}
            {images.length > 0 && (
              <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4">
                {images.map((image) => (
                  <div key={image.id} className="relative group">
                    <img
                      src={image.url}
                      alt={image.name}
                      className="w-full h-24 object-cover rounded-lg border border-gray-200"
                    />
                    <button
                      type="button"
                      onClick={() => removeImage(image.id)}
                      className="absolute top-1 right-1 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      <X className="h-3 w-3" />
                    </button>
                    <p className="text-xs text-gray-500 mt-1 truncate">{image.name}</p>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Form Actions */}
          <div className="flex justify-end space-x-3 pt-4 border-t border-gray-200">
            <button
              type="button"
              onClick={toggleTaskInput}
              className="btn-secondary"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn-primary flex items-center space-x-2"
              disabled={!description.trim() || queuedStages.length === 0}
            >
              <Plus className="h-4 w-4" />
              <span>Create Task</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default TaskInput;