# Bug: Fix Command Editor UI Issues

## Metadata
issue_number: `004`
adw_id: `jkl012`
issue_json: `{"title": "Fix Command Editor UI Issues", "body": "Ensure after I click edit it is maximised not like this minimal state. Need not repeat the title again just /command is sufficient. The content within the file is mocked and the real content is not loaded. Also I dont see advanced styling options which we added for the input task as well. Even the token count is not real. Lets have real sync of the data. Instead of copying the file content lets have almost one to one reference of the content of this file. /bug -> /slash commands lets them be bolded."}`

## Bug Description
The Commands Palette and Command Editor have multiple critical issues:
1. Modal doesn't open in maximized/fullscreen mode by default when clicking edit
2. Header shows redundant information - displays both slash command name and display name instead of just bold slash command
3. Missing advanced styling options (MDEditor) that exist in TaskInput component
4. Slash commands in display are not bolded as requested
5. Users want WYSIWYG editing capability - editing directly in preview mode with automatic markdown generation hidden from view

## Problem Statement
The Commands Palette and Command Editor interface provide a poor user experience due to:
- Non-maximized default view making editing difficult
- Confusing header information display
- Lack of rich text editing capabilities available in other parts of the application
- Slash commands not being bolded as requested
- Missing WYSIWYG editing capability for direct preview editing

## Solution Statement
Implement comprehensive fixes to the Commands Palette and Command Editor:
- Set fullscreen mode as default when opening editor
- Simplify header to show only bold slash command name
- Integrate MDEditor for rich text editing capabilities matching TaskInput
- Apply bold styling to slash commands throughout the interface
- Implement WYSIWYG editing mode that allows direct editing in rendered preview with hidden markdown syntax generation

## Steps to Reproduce
1. Open the Kanban application
2. Click on any command card to open Commands Palette
3. Click "Edit" button on any command
4. Observe the modal opens in minimal state instead of maximized
5. Notice header shows both "/command" and "Display Name"
6. Notice the basic textarea lacks rich text editing features
7. Verify slash commands are not bolded in the interface
8. Note the lack of WYSIWYG editing capability for direct preview editing

## Root Cause Analysis
1. **Modal State**: CommandEditor initializes with `isFullscreen: false` instead of `true`
2. **Header Display**: Component shows both slash name and display name instead of just bold slash name
3. **Editor Type**: Uses basic `<textarea>` instead of MDEditor like TaskInput
4. **Styling**: Slash commands lack bold CSS styling throughout the interface
5. **WYSIWYG Capability**: Current editor lacks WYSIWYG editing mode for direct preview editing

## Relevant Files
Use these files to fix the bug:

- `src/components/CommandEditor.jsx` - Main editor component that needs UI fixes and fullscreen default
- `src/components/CommandsPalette.jsx` - Parent component that opens the editor, needs header display fixes
- `src/components/TaskInput.jsx` - Reference for MDEditor implementation and styling
- `src/styles/kanban.css` - CSS styles for ensuring proper bold styling of slash commands

### New Files
- `.claude/commands/e2e/test_enhanced_commands_editor.md` - E2E test file to validate the command editor fixes

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Fix Modal Fullscreen Default State
- Update CommandEditor component to initialize `isFullscreen: true` by default when opening
- Ensure proper CSS classes apply for fullscreen mode from the start
- Test modal opens in maximized state when clicking edit button

### Simplify Header Display
- Modify CommandEditor header to show only the slash command name in bold
- Remove the duplicate display name from the header section
- Apply bold styling to slash command names using CSS classes

### Integrate Rich Text Editor
- Replace basic textarea in CommandEditor with MDEditor component
- Import and configure MDEditor similar to TaskInput implementation
- Ensure markdown preview and editing capabilities work properly
- Maintain existing save and commit functionality with new editor

### Implement WYSIWYG Editing Mode
- Research and evaluate WYSIWYG markdown editor options compatible with React (e.g., @uiw/react-md-editor with enhanced configurations)
- Add a new editing mode called 'wysiwyg' that allows direct editing in rendered preview
- Implement automatic markdown syntax generation in the background without showing raw syntax to users
- Update the mode toggle buttons to include the WYSIWYG option
- Ensure the WYSIWYG editor maintains all existing functionality (save, commit, token counting)

### Apply Bold Styling to Slash Commands
- Add CSS classes for bold styling of slash commands throughout the interface
- Update CommandsPalette to display slash commands in bold
- Ensure consistent bold styling across all command displays
- Test bold styling appears correctly in all contexts

### Create E2E Test File
- Read `.claude/commands/e2e/test_basic_query.md` and `.claude/commands/test_e2e.md` and create a new E2E test file in `.claude/commands/e2e/test_enhanced_commands_editor.md` that validates all the command editor fixes are working correctly, including fullscreen mode, rich text editing, WYSIWYG mode, and bold slash command display. Include specific steps to prove each bug is fixed with screenshots.

### Run Validation Commands
- Execute all validation commands to ensure fixes work properly and no regressions are introduced

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

- `npm run dev` - Start development server to test the application
- Manual testing: Open Commands Palette, click Edit on a command, verify fullscreen mode, rich text editor, WYSIWYG mode, and bold slash commands
- `npm run build` - Build the application to ensure no build errors
- `npm run lint` - Run linting to ensure code quality standards
- Read `.claude/commands/test_e2e.md`, then read and execute your new E2E `.claude/commands/e2e/test_enhanced_commands_editor.md` test file to validate this functionality works

## Notes
- The MDEditor component from `@uiw/react-md-editor` is already available in the project as seen in TaskInput
- Ensure all changes maintain existing functionality for save and commit operations
- Bold styling for slash commands should be consistent across the entire application interface
- Test thoroughly to ensure the fixes don't break existing command execution functionality
- The WYSIWYG implementation should maintain backward compatibility with existing editing modes
- Consider using a well-established WYSIWYG markdown editor library rather than building from scratch
- Ensure the new editing mode properly handles token counting and file saving