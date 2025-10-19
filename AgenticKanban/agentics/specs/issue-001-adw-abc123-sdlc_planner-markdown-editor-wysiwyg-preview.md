# Bug: Markdown Editor WYSIWYG Preview Mode

## Metadata
issue_number: `001`
adw_id: `abc123`
issue_json: `{"title": "Markdown Editor WYSIWYG Preview", "body": "As soon as I click on edit, I don't want to see the markdown view. It should show me the preview mode with no markdown symbols. I can directly edit in the preview mode. Don't make it dark in preview mode. If you need, feel free to get a good markdown editor that has a great preview."}`

## Bug Description
When users click the "Edit" button in the CommandEditor component, they are shown a raw markdown editor with markdown symbols visible. Users expect to see a rendered preview mode without markdown symbols where they can edit content directly (WYSIWYG - What You See Is What You Get editing). The current preview mode is basic and doesn't allow inline editing, forcing users to work with raw markdown syntax.

## Problem Statement
The current markdown editor implementation uses `@uiw/react-md-editor` with a simple preview toggle that switches between raw markdown editing and basic text preview. Users want a true WYSIWYG editing experience where they can edit content in a rendered preview mode without seeing markdown syntax, similar to modern editors like Notion or Google Docs.

## Solution Statement
Replace or enhance the current markdown editor implementation to provide WYSIWYG editing capabilities. This will involve either upgrading the current `@uiw/react-md-editor` configuration to use its preview editing mode, or integrating a more advanced markdown editor that supports inline/WYSIWYG editing with light theme styling.

## Steps to Reproduce
1. Navigate to the Kanban board application
2. Open any command for editing (click on a command in the CommandsPalette)
3. Click the "Edit" button to switch from preview mode
4. Observe that raw markdown with symbols is displayed instead of a rendered, editable preview

## Root Cause Analysis
The current implementation in `CommandEditor.jsx` uses `@uiw/react-md-editor` with `preview="edit"` mode, which shows raw markdown syntax. The preview toggle only switches between this raw markdown editor and a very basic text preview (`renderMarkdownPreview()` function) that doesn't support editing. The component lacks true WYSIWYG editing capabilities where users can edit rendered content directly.

## Relevant Files
Use these files to fix the bug:

- `src/components/CommandEditor.jsx` - Main markdown editor component that needs WYSIWYG editing implementation
- `package.json` - May need to update or add markdown editor dependencies for better WYSIWYG support
- `src/styles/kanban.css` - For styling the light theme preview mode and ensuring it's not dark
- `src/index.css` - For global styling adjustments if needed
- `.claude/commands/test_e2e.md` - For understanding E2E testing framework
- `.claude/commands/e2e/test_basic_query.md` - For understanding E2E test file format

### New Files
- `.claude/commands/e2e/test_markdown_editor_wysiwyg.md` - E2E test to validate WYSIWYG editing functionality

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Research and Choose WYSIWYG Solution
- Research `@uiw/react-md-editor` advanced configuration options for WYSIWYG editing
- Evaluate alternative markdown editors with better WYSIWYG support (such as `@uiw/react-md-editor` with `preview="preview"` mode, or other editors like `react-markdown-editor-lite`)
- Choose the best solution that provides true WYSIWYG editing with light theme support

### Update Markdown Editor Implementation
- Modify `CommandEditor.jsx` to implement WYSIWYG editing mode
- Configure the editor to show rendered content by default when "Edit" is clicked
- Ensure the editor uses a light theme and doesn't appear dark
- Update the preview toggle logic to switch between WYSIWYG editing and read-only preview
- Maintain existing functionality for save, commit, and other editor features

### Style and Theme Configuration
- Update CSS styling in `src/styles/kanban.css` to ensure light theme for the editor
- Add any necessary CSS overrides to prevent dark mode styling
- Ensure the editor integrates well with the existing UI design

### Testing Implementation
- Read `.claude/commands/e2e/test_basic_query.md` and `.claude/commands/test_e2e.md` to understand E2E testing format
- Create a new E2E test file `.claude/commands/e2e/test_markdown_editor_wysiwyg.md` that validates:
  - Opening the command editor
  - Switching to edit mode shows WYSIWYG preview
  - Content can be edited directly in the rendered view
  - No raw markdown symbols are visible during editing
  - Light theme is maintained (not dark)
  - Save functionality works correctly
  - Take screenshots to prove WYSIWYG editing works

### Validation and Quality Assurance
- Run the `Validation Commands` to ensure no regressions
- Execute the new E2E test to validate WYSIWYG functionality
- Test various markdown content types (headers, links, lists, etc.) to ensure proper rendering and editing

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

- `npm run dev` - Start the development server to test the changes
- `npm run lint` - Ensure code quality and no linting errors
- `npm run build` - Verify the application builds successfully without errors
- `npm run test` - Run any existing tests to ensure no regressions
- Manual testing: Open command editor, click "Edit", verify WYSIWYG mode is active with light theme
- Read `.claude/commands/test_e2e.md`, then read and execute the new `.claude/commands/e2e/test_markdown_editor_wysiwyg.md` test file to validate WYSIWYG functionality works

## Notes
- Focus on user experience - the goal is seamless WYSIWYG editing without markdown syntax visibility
- Maintain light theme throughout the editing experience
- Preserve all existing editor functionality (save, commit, copy, etc.)
- Consider performance impact of rendering markdown in real-time during editing
- Ensure accessibility is maintained in the new editing mode
- Test with various types of markdown content to ensure robust editing experience