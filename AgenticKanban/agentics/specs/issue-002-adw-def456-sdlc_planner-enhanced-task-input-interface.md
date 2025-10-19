# Bug: Enhanced Task Input Interface - Work Item Types and Rich Text Editor

## Metadata
issue_number: `002`
adw_id: `def456`
issue_json: `{"title": "Enhanced Task Input Interface", "body": "The input for task needs to not have title field where users can just start entering prompt. Should include radio button options (Feature, Chore, Bug, Patch) and the ADW pipelines should not be dropdown but actual primitive stages like plan, Implement, Test, Review, Document, PR that can be queued to control the flow of execution. Also need advanced editor capabilities with text styling (bold, italics, underline) and image support with annotation capabilities."}`

## Bug Description
The current task input modal has several usability and functionality issues:
1. **Required title field**: Users must enter a title before entering the task description, creating unnecessary friction
2. **Limited work item classification**: No way to specify the type of work (Feature, Chore, Bug, Patch)
3. **Inflexible pipeline selection**: ADW Pipeline is a dropdown with predefined workflows, lacking granular control
4. **Basic text editor**: Description field is a plain textarea without rich text formatting capabilities
5. **No media support**: Cannot add images or annotations to provide visual context for tasks

## Problem Statement
The task creation experience lacks flexibility and modern rich text editing capabilities. Users need a more streamlined workflow that allows:
- Direct prompt entry without mandatory title
- Work item type classification
- Granular stage control and queueing
- Rich text formatting and image annotation

## Solution Statement
Transform the task input interface into a modern, flexible system with:
- Optional title field that defaults to empty
- Radio button work item type selection (Feature, Chore, Bug, Patch)
- Checkbox-based stage selection allowing users to queue specific stages
- Rich text editor with formatting controls (bold, italic, underline)
- Image upload and annotation capabilities

## Steps to Reproduce
1. Open the application
2. Click the "+" button to create a new task
3. Observe the "Create New Task" modal
4. Note the required "Task Title" field
5. Note the basic textarea for description
6. Note the ADW Pipeline dropdown with fixed options
7. Attempt to format text or add images (not possible)

## Root Cause Analysis
The current TaskInput component (`src/components/TaskInput.jsx`) is designed with:
- Fixed form structure requiring title input
- Dropdown-based pipeline selection tied to adwService pipelines
- Basic HTML textarea without rich text capabilities
- No image handling or annotation features
- Hard-coded form validation requiring title

## Relevant Files
Use these files to fix the bug:

- `src/components/TaskInput.jsx` - Main task input modal component that needs complete redesign
- `src/stores/kanbanStore.js` - Task creation logic and validation that needs updating for new workflow
- `src/services/adwService.js` - Pipeline service that may need extension for stage queueing
- `src/styles/kanban.css` - Styling that needs enhancement for new UI elements
- `package.json` - May need rich text editor dependencies
- `src/index.css` - Global styles that may need updates for rich text editor
- `.claude/commands/conditional_docs.md` - Documentation requirements
- `.claude/commands/test_e2e.md` - E2E testing framework documentation
- `.claude/commands/e2e/test_basic_query.md` - Example E2E test structure

### New Files
- `.claude/commands/e2e/test_enhanced_task_input.md` - E2E test for the enhanced task input interface

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Install Rich Text Editor Dependencies
- Research and install appropriate rich text editor library (e.g., Quill, Draft.js, or TinyMCE)
- Add image handling dependencies if needed
- Update package.json with new dependencies

### Update Data Model and Validation
- Modify kanbanStore.js to make title optional in task creation
- Add workItemType field to task data model (Feature, Chore, Bug, Patch)
- Add queuedStages array to task data model for stage selection
- Update task validation to remove title requirement
- Add validation for workItemType and queuedStages

### Redesign TaskInput Component Structure
- Remove required asterisk and validation from title field
- Replace ADW Pipeline dropdown with work item type radio buttons (Feature, Chore, Bug, Patch)
- Add stage selection interface with checkboxes for primitive stages (Plan, Implement, Test, Review, Document, PR)
- Implement stage queueing logic to allow users to select multiple stages

### Implement Rich Text Editor
- Replace basic textarea with rich text editor component
- Add formatting toolbar with bold, italic, underline options
- Ensure editor integrates properly with form submission
- Style editor to match application design system

### Add Image Upload and Annotation
- Implement image upload functionality with drag-and-drop support
- Add basic annotation tools for uploaded images
- Handle image storage and display within tasks
- Ensure images are properly saved and retrieved

### Update Styling and Responsive Design
- Update kanban.css with styles for new UI elements
- Ensure radio buttons and checkboxes follow design system
- Style rich text editor toolbar and controls
- Make interface responsive across different screen sizes
- Add proper focus states and accessibility features

### Create E2E Test
- Read `.claude/commands/e2e/test_basic_query.md` and `.claude/commands/e2e/test_complex_query.md` and create a new E2E test file in `.claude/commands/e2e/test_enhanced_task_input.md` that validates the enhanced task input interface works correctly, including work item type selection, stage queueing, rich text formatting, and image upload functionality. Include specific steps to prove all new features work and take screenshots to document the improvements.

### Run Validation Commands
- Execute all validation commands to ensure the bug is fixed with zero regressions

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

- `npm install` - Install any new dependencies
- `npm run dev` - Start development server to test changes
- `npm run build` - Verify application builds successfully
- `npm run lint` - Ensure code quality standards are met
- Manual testing of task creation workflow with new interface
- Test work item type selection functionality
- Test stage queueing and selection
- Test rich text formatting (bold, italic, underline)
- Test image upload and annotation features
- Test form submission with optional title
- Test responsive design on different screen sizes
- Read `.claude/commands/test_e2e.md`, then read and execute your new E2E `.claude/commands/e2e/test_enhanced_task_input.md` test file to validate this functionality works.

## Notes
- Consider using a well-established rich text editor library to avoid reinventing formatting functionality
- Ensure image uploads are handled efficiently and include appropriate file size limits
- The stage queueing system should integrate with the existing stage progression service
- Maintain backward compatibility with existing tasks that have titles
- Consider adding auto-save functionality for the rich text editor
- Image annotation features should be intuitive and include basic drawing/text overlay tools
- Test thoroughly with different browsers and devices to ensure consistent experience