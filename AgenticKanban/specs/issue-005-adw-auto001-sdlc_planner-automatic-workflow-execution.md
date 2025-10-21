# Chore: Automatic Workflow Execution

## Metadata
issue_number: `005`
adw_id: `auto001`
issue_json: `{"title": "Make workflow execution automatic/headless", "body": "After creating a task, the application shows a modal asking to copy and run a command in terminal. Since the kanban board already has the project path, this should execute automatically without requiring manual terminal commands."}`

## Chore Description
Replace the manual command execution modal with automatic workflow execution. Currently, when a user creates a task in the Kanban board, they are presented with a modal dialog containing a command that must be copied and run manually in their terminal. Since the application already has access to the project path and filesystem APIs, the workflow should execute automatically without user intervention.

## Relevant Files
Use these files to resolve the chore:

- `src/components/CommandDisplay.jsx` - The modal component that shows the manual command execution instructions, needs to be replaced or modified
- `src/stores/kanbanStore.js` - Contains the `createTaskWithCommand` function that shows the command modal, needs to be updated to execute automatically
- `src/utils/commandGenerator.js` - Contains command generation utilities that may need modification for automatic execution
- `package.json` - May need to check if Node.js child_process or similar execution capabilities are available

### New Files
- `src/utils/workflowExecutor.js` - New utility to handle automatic execution of ADW workflow commands
- `src/components/ExecutionStatus.jsx` - Optional component to show real-time execution status instead of the command modal

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Research Current Implementation
- Analyze the current command generation and modal display flow
- Understand how the project path and ADW commands are structured
- Review the File System Access API usage for project directory access

### Create Workflow Executor Utility
- Create `src/utils/workflowExecutor.js` with automatic command execution functionality
- Implement subprocess execution for ADW orchestrator commands using Node.js APIs
- Add error handling and status reporting for command execution
- Ensure proper working directory handling based on project path

### Update Kanban Store
- Modify `createTaskWithCommand` function to use automatic execution instead of showing modal
- Remove `showCommandModal`, `currentCommand`, and `currentTaskData` state management
- Update task creation flow to immediately start workflow execution
- Add execution status tracking to task metadata

### Replace Command Display Modal
- Either remove `CommandDisplay.jsx` entirely or convert it to show execution status
- If keeping as status display, update to show real-time execution progress
- Remove manual command copying functionality

### Update Task Input Flow
- Ensure task creation immediately triggers workflow execution
- Add loading states and progress indicators during execution
- Handle execution errors gracefully with user feedback

### Add Configuration Option
- Add user preference setting to toggle between automatic and manual execution
- Implement fallback to manual modal if automatic execution fails
- Store preference in local storage for persistence

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `npm run dev` - Start the development server and verify the application loads
- Create a test task through the UI and verify it executes automatically without showing the command modal
- Verify that task status updates properly during automatic execution
- Check browser console for any execution errors or warnings
- Test error handling by creating a task with invalid parameters
- Verify that polling still works correctly for automatically executed tasks

## Notes
- The File System Access API should provide sufficient access to execute commands in the project directory
- Consider adding a toggle option for users who prefer manual command execution
- Ensure backward compatibility with existing task polling and state management
- The Python ADW orchestrator script execution may require Node.js child_process APIs
- Add proper error boundaries and user feedback for execution failures